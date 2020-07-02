

import json
import itertools
from lib.utils.mytime import UtilTime
from lib.utils.exceptions import PubErrorCustom

from app.cp.models import CpTermListHistory,CpTermList
from django.db.models import Q
from app.cache.utils import RedisCaCheHandler
from app.order.models import Order
from app.cp.models import CpTermListHistory
from app.user.models import Users
from decimal import *



def countTotTerm(opentime,termnum):

    """
        计算总期数
            如果是时间分段那么要算时间跨度+1
    """

    if opentime == 'all':
        M = 24 * 60
        if M % termnum >0:
            PubErrorCustom("根据开奖时间和期数间隔时间无法精确算出总期数，请调整后提交!")

        return int(M / termnum)
    else:
        ut = UtilTime()
        tot = 0
        C = opentime.split('|')
        for item in C:
            start_time = item.split('-')[0]
            end_time = item.split('-')[1]

            a = ut.arrow_to_string(ut.string_to_arrow(string_s=end_time, format_v="HHmm").shift(hours=-(int(start_time[0:2])), minutes=-(int(start_time[2:4]))),
                                   "HH:mm")
            tot += int(a.split(":")[0]) * 60 + int(a.split(":")[1])

        return tot/20+len(C)

def count_end_time(opentime,endtime):
    """
    计算倒计时时间
    :param cp:
    :return:
    """
    p = (int(opentime[:2]) * 3600) + (int(opentime[2:]) * 60) - endtime
    return "%02d%02d%02d" % ((p // 3600), (p % 3600 // 60),(p % 3600 % 60))

def get_autoid(cp,i):
    rules = json.loads(cp.coderule)
    if rules['after']['type'] == '0':
        term = "%0{}d".format(int(rules['after']['value']))
    else:
        raise PubErrorCustom("期数生成规则有误!")

    return term % (i)

def create_task_table(cp):

    tables = []

    if cp.opentime == 'all':

        alltimem = 1440

        s = "0001"
        d = (int(s[:2]) * 60) + int(s[2:])

        count = 0

        while d <= alltimem:
            count += 1
            tables.append({"id":get_autoid(cp,count),"opentime":s if s!='2400' else '0000',"endtime":count_end_time(s,cp.endtime)})
            p = d + cp.termnum
            s = "%02d%02d" % ((p // 60), (p % 60))
            d = (int(s[:2]) * 60) + int(s[2:])
    else:

        count1 = 0
        for item in cp.opentime.split("|"):

            start_time = item.split('-')[0]
            end_time = item.split('-')[1]

            alltimem = (int(end_time[:2]) * 60) + int(end_time[2:])

            s = start_time
            d = (int(s[:2]) * 60) + int(s[2:])
            count = 0

            while d <= alltimem:
                count += 1
                count1+=1
                tables.append({"id": get_autoid(cp,count1), "opentime": s, "endtime": count_end_time(s, cp.endtime)})
                p = d + 20
                s = "%02d%02d" % ((p // 60), (p % 60))
                d = (int(s[:2]) * 60) + int(s[2:])

    print(len(tables))
    return tables

def getDownTerm(today,autoid):
    return "{}{}".format(today,autoid)


def get_downdata(cp):

    downterm,downtime = count_downtime(cp)

    return {
        "downterm" :downterm,
        "downtime":downtime
    }

def get_cp_term_coderules_before(cp,ut):
    if cp['coderule']['before']['type'] == '0':
        today = ut.arrow_to_string(format_v=cp['coderule']['before']['value'])
        tomorrow = ut.arrow_to_string(ut.today.shift(days=1), format_v=cp['coderule']['before']['value'])
        return today,tomorrow
    else:
        raise PubErrorCustom("暂不支持!")

def count_time_strand(t):

    if t:
        ut = UtilTime()

        today = ut.today

        dissday = (t - today)

        days = dissday.days
        seconds = dissday.seconds

        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        return {
            "d":days,
            "h":hours,
            "m":minutes,
            "s":seconds
        }
    else:
        return {
            "d":0,
            "h":0,
            "m":0,
            "s":0
        }

def count_downtime(cp):

    if cp.ispc=='0':
        try:
            ctlObj = CpTermList.objects.get(cpid=cp['id'])
        except CpTermList.DoesNotExist:
            ctlObj = None

        currterm = ctlObj.nextterm if ctlObj else None

        return currterm,count_time_strand(ctlObj.nexttime if ctlObj else None)
    else:
        currterm=""
        ut = UtilTime()
        today,tomorrow = get_cp_term_coderules_before(cp,ut)
        currtime = ut.arrow_to_string(format_v="HHmmss")
        tables=json.loads(cp['tasktimetable'])['tables']
        tables.sort(key=lambda k: (k.get('id')), reverse=False)
        isFlag = False
        for tItem in tables:
            item = tItem['endtime']
            if int(currtime) < int(item):
                currterm=getDownTerm(today,tItem['id'])
                end_time = (int(item[:2]) * 60 * 60) + (int(item[2:4]) * 60) + int(item[4:])
                start_time = (int(currtime[:2]) * 60 * 60) + (int(currtime[2:4]) * 60) + int(currtime[4:])
                currtime = end_time - start_time
                isFlag = True
                break

        if not isFlag:
            currterm = getDownTerm(tomorrow, tables[0]['id'])
            item = tables[0]['endtime']
            end_time = (int(item[:2]) * 60 * 60) + (int(item[2:4]) * 60) + int(item[4:])
            start_time = (int(currtime[:2]) * 60 * 60) + (int(currtime[2:4]) * 60) + int(currtime[4:])
            currtime = end_time + (1 * 24 * 60 * 60) - start_time

        return currterm,{"h": currtime // 3600, "m": currtime % 3600 // 60, "s": currtime % 60}


def showdatetime(createtime):
    ut = UtilTime()
    today = ut.arrow_to_string(format_v="YYYY-MM-DD")
    t = ut.timestamp_to_arrow(createtime)
    if today == ut.arrow_to_string(t,format_v="YYYY-MM-DD"):
        before = "今天"
    elif today == ut.arrow_to_string(t.shift(days=1),format_v="YYYY-MM-DD"):
        before = "昨天"
    else:
        before = ut.arrow_to_string(t)[5:10].replace('-','月')+'日'

    return before + ut.arrow_to_string(t)[10:]



def get_open_history(cp):

    ut = UtilTime()

    res = CpTermListHistory.objects.filter(cpid=cp['id']).filter(~Q(cpno='')).order_by('-createtime')[:10]
    data=[]
    if res.exists:
        for item in res:
            data.append({
                "cpno":[ no for no in item.cpno.split(",") ],
                "term":item.term,
                "createtime" : ut.timestamp_to_string(item.createtime),
                "createtime_format" :  showdatetime(item.createtime)
            })
    return data



def get_open_term(cp):

    pass

def get_next_term(cpid):
    try:
        return  CpTermList.objects.get(cpid=cpid).nextterm
    except CpTermList.DoesNotExist:
        raise PubErrorCustom('系统错误!')


def get_rate(rules):

    RCaCheClass = RedisCaCheHandler()


    if rules['ratetype'] == '2':
        rates = []
        for item in rules['rates']:
            RCaCheClass.customInit(
                method="get",
                serialiers="CpGamesModelSerializerToRedis",
                table="cpgames",
                must_key_value=item
            )
            tmpObj = RCaCheClass.run()
            rates.append(tmpObj['rules']['rate'])
        rates.sort()
        return rates
    elif rules['ratetype'] == '3':
        rates = []
        for item in rules['rate'].split(','):
            rates.append(item)
        rates.sort()
        return rates
    else:
        return rules['rate']

def winHandler(orderid):

    try:
        order = Order.objects.select_for_update().get(orderid=orderid)
        games = RedisCaCheHandler(
            method="get",
            serialiers="CpGamesModelSerializerToRedis",
            table="cpgames",
            must_key_value=order.gamesid).run()
        if not games:
            raise PubErrorCustom("无此玩法!")

        try:
            cpno = CpTermListHistory.objects.get(cpid=order.cpid,term=order.term).cpno
        except CpTermListHistory.DoesNotExist:
            return False

        if wincode_run(order,games,cpno):
            Order.status = '1'
            user = Users.objects.get(userid=order.userid)
            user.bal += order.amount
            user.save()
            order.save()
            return True

    except Order.DoesNotExist:
        raise PubErrorCustom("无此订单!")

    return False

def compose_y(no):
    print(no)
    d = []
    for item in itertools.product(*no):
        d.append(item)

    return d

def wincode_run(order,games,confirmNo):
    context = {}
    code = games['wincode']
    exec(code, context)
    cpNo = compose_y([item['cp'] for item in order.cpno])
    return context["customFuncForCpWin"](cpNo=cpNo,confirmNo=confirmNo)