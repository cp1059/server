

import json

from lib.utils.mytime import UtilTime
from lib.utils.exceptions import PubErrorCustom

from app.cp.models import CpTermListHistory,CpTermList


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


def create_task_table(cp):

    tables = []

    if cp.opentime == 'all':

        alltimem = 1440

        s = "0000"
        d = (int(s[:2]) * 60) + int(s[2:])

        count = 0

        while d < alltimem:
            count += 1
            tables.append(s)
            p = d + cp.termnum
            s = "%02d%02d" % ((p // 60), (p % 60))
            d = (int(s[:2]) * 60) + int(s[2:])
    else:

        for item in cp.opentime.split("|"):

            start_time = item.split('-')[0]
            end_time = item.split('-')[1]

            alltimem = (int(end_time[:2]) * 60) + int(end_time[2:])

            s = start_time
            d = (int(s[:2]) * 60) + int(s[2:])
            count = 0

            while d <= alltimem:
                count += 1
                tables.append(s)
                p = d + 20
                s = "%02d%02d" % ((p // 60), (p % 60))
                d = (int(s[:2]) * 60) + int(s[2:])

    return tables


def count_downtime(cp):

    ut = UtilTime()

    currtime = ut.arrow_to_string(format_v="HHmmss")
    tables = json.loads(cp['tasktimetable'])['tables']
    tables.sort()
    isFlag = False
    for item in tables:
        if int(currtime[:4]) < int(item):
            print(currtime,item)
            end_time = (int(item[:2])*60*60) + (int(item[2:])*60)
            start_time = (int(currtime[:2])*60*60) + (int(currtime[2:4])*60) + int(currtime[4:])
            currtime = end_time - start_time
            isFlag = True
            break

    if not isFlag:
        end_time = (int(item[:2]) * 60 * 60) + (int(item[2:]) * 60)
        start_time = (int(currtime[:2]) * 60 * 60) + (int(currtime[2:4]) * 60) + int(currtime[4:])
        currtime = end_time + (1 * 24 * 60 * 60) - start_time

    return {"h":currtime // 3600,"m":currtime % 3600 // 60,"s":currtime % 60}

def get_open_history(cp):

    res = CpTermListHistory.objects.filter(cpid=cp['id']).order_by('-createtime')[:5]
    data=[]
    if res.exists:
        for item in res:
            data.append({
                "cpno":[ no for no in item.cpno.split(",") ],
                "term":item.term[7:]
            })
    return data

def get_open_term(cp):

    res=None
    try:
        res = CpTermList.objects.get(cpid=cp['id'])
    except CpTermList.DoesNotExist:
        pass

    return {
        "nextterm":res.nextterm,
        "cpno": [no for no in res.cpno.split(",")],
    } if res else {}

def get_next_term(cpid):
    try:
        return  CpTermList.objects.get(cpid=cpid).nextterm
    except CpTermList.DoesNotExist:
        raise PubErrorCustom('系统错误!')

