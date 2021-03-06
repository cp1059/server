
import json
from rest_framework.decorators import list_route
from rest_framework import viewsets
from lib.core.decorator.response import Core_connector
from lib.utils.exceptions import PubErrorCustom
from app.order.models import Order
from app.cp.utils import get_next_term
from app.cache.utils import RedisCaCheHandler
from app.user.models import Users
from decimal import *
from app.order.serialiers import OrderSerializer
from app.cp.utils import get_rate,get_downdata,winHandler
from lib.utils.mytime import UtilTime

class OrderAPIView(viewsets.ViewSet):


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True)
    def orderWin(self,request):
        cpid = request.data.get("cpid",None)
        term = request.data.get("term",None)

        if not cpid:
            raise PubErrorCustom("cpid is void!")
        if not term:
            raise PubErrorCustom("term is void!")
        pass

    @list_route(methods=['POST'])
    @Core_connector(isPasswd=True,isTicket=True,isTransaction=True)
    def createOrder(self, request):

        print(request.data_format)

        cps = request.data_format.get("cp",[])

        if not len(cps):
            raise PubErrorCustom("无下单数据!")

        try:
            user = Users.objects.select_for_update().get(userid=request.user['userid'],status='0')
        except Users.DoesNotExist:
            raise PubErrorCustom("非法用户!")

        RCaCheClassGames = RedisCaCheHandler()

        amount = Decimal(0.0)
        for cp in cps:

            curramount = cp['num'] * Decimal(str(cp['single']))
            amount += curramount

            RCaCheClassGames.customInit(
                method="get",
                serialiers="CpModelSerializerToRedis",
                table="cp",
                must_key_value=cp['cpid']
            )
            cpStatic = RCaCheClassGames.run()
            if not cpStatic:
                raise PubErrorCustom("无此彩票!")
            if cpStatic['status']=='1':
                raise PubErrorCustom("彩票{}已停售".format(cpStatic.name))
            elif cpStatic['status']=='2':
                raise PubErrorCustom("彩票{}正在维护".format(cpStatic.name))

            RCaCheClassGames.customInit(
                method="get",
                serialiers="CpGamesModelSerializerToRedis",
                table="cpgames",
                must_key_value=cp['gamesid']
            )
            games = RCaCheClassGames.run()
            if not games:
                raise PubErrorCustom("无此玩法!")

            rate = get_rate(games['rules'])
            if isinstance(rate,list) :
                rate.sort()
                rate_tmp = ""
                for item in rate:
                    rate_tmp += "{},".format(item)
                rate=rate_tmp[:-1]

            print(rate)

            Order.objects.create(**{
                "userid":request.user['userid'],
                "amount":curramount,
                "num":cp['num'],
                "term":get_downdata(cpStatic)['downterm'],
                "no":json.dumps({'no':cp['cp']}),
                "cpid":cp['cpid'],
                "gamesid":cp['gamesid'],
                "rate":rate
            })

        if amount > user.bal:
            raise PubErrorCustom("余额不足!")

        user.bal -= amount
        user.save()

        return None


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getOrder(self, request):

        query_format = str()
        query_params = list()

        page = int(request.query_params_format.get("page",1))
        page_size = int(request.query_params_format.get("page_size",10))

        query_format = query_format + " and t1.userid =%s"
        query_params.append(request.user['userid'])

        if request.query_params_format.get("cpid"):
            query_format = query_format + " and t1.cpid =%s"
            query_params.append(request.query_params_format.get("cpid"))

        if request.query_params_format.get("status"):
            query_format = query_format + " and t1.status =%s"
            query_params.append(request.query_params_format.get("status"))

        limit_format = " limit %d,%d"%((page-1)*page_size,page_size)

        orders = Order.objects.raw("""
            SELECT t1.*,t2.name as cpname,t2.url as cpurl,t3.name as gamename,t4.name as minitypename FROM `order` as t1
            INNER JOIN `cp` as t2 ON t1.cpid = t2.id
            INNER JOIN `cpgames` as t3 ON t1.gamesid = t3.typeid
            INNER JOIN `cpminitype` as t4 ON t3.minitypeid = t4.typeid
            WHERE 1=1 %s order by t1.createtime desc %s 
        """% (query_format,limit_format), query_params)

        return { "data" : OrderSerializer(orders,many=True).data }

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True)
    def getOrderWeb(self, request):

        query_format = str()
        query_params = list()

        if request.query_params_format.get("cpid"):
            query_format = query_format + " and t1.cpid =%s"
            query_params.append(request.query_params_format.get("cpid"))

        if request.query_params_format.get("status"):
            query_format = query_format + " and t1.status =%s"
            query_params.append(request.query_params_format.get("status"))

        if request.query_params_format.get("userid"):
            query_format = query_format + " and t1.userid =%s"
            query_params.append(request.query_params_format.get("userid"))

        if request.query_params_format.get("orderid"):
            query_format = query_format + " and t1.orderid =%s"
            query_params.append(request.query_params_format.get("orderid"))

        if request.query_params_format.get("startdate") and request.query_params_format.get("enddate"):
            query_format = query_format + " and t1.createtime>={} and t1.createtime<={}".format(
                UtilTime().string_to_timestamp(request.query_params_format.get("startdate")),
                UtilTime().string_to_timestamp(request.query_params_format.get("enddate"))
            )

        # limit_format = " limit %d,%d" % ((page - 1) * page_size, page_size)

        orders = list(Order.objects.raw("""
                SELECT t1.*,t2.name as cpname,t2.url as cpurl,t3.name as gamename,t4.name as minitypename FROM `order` as t1
                INNER JOIN `cp` as t2 ON t1.cpid = t2.id
                INNER JOIN `cpgames` as t3 ON t1.gamesid = t3.typeid
                INNER JOIN `cpminitype` as t4 ON t3.minitypeid = t4.typeid
                WHERE 1=1 %s order by t1.createtime desc
            """ % (query_format), query_params))

        page=int(request.query_params_format.get('page'))
        page_size=int(request.query_params_format.get('page_size'))
        page_start = page_size * page - page_size
        page_end = page_size * page

        count = len(orders)

        return {"data": OrderSerializer(orders[page_start:page_end], many=True).data,"count":count}

    @list_route(methods=['POST'])
    @Core_connector(isPasswd=True,isTicket=True,isTransaction=True)
    def delOrder(self, request):

        orderid = request.data_format.get("orderid",None)

        try:
            order = Order.objects.select_for_update().get(orderid=orderid)
            if order.status == '1':
                raise PubErrorCustom("此订单已中奖!")
            elif order.status == '2':
                raise PubErrorCustom("此订单已撤单!")
            elif order.status == '3':
                raise PubErrorCustom("此订单未中奖!")
        except Users.DoesNotExist:
            raise PubErrorCustom("无此订单!")

        try:
            user = Users.objects.select_for_update().get(userid=request.user['userid'],status='0')
        except Users.DoesNotExist:
            raise PubErrorCustom("非法用户!")

        order.status = '2'
        order.save()

        user.bal += order.amount
        user.save()

        return None


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True)
    def getDataCount(self, request):

        pass
        data={
            "amount" : 0.0,
            "zjamount":0.0
        }

        ut = UtilTime()

        if request.query_params_format.get("startdate") and request.query_params_format.get("enddate"):
            start = ut.string_to_timestamp(request.query_params_format.get("startdate"))
            end = ut.string_to_timestamp(request.query_params_format.get("enddate"))
        else:
            start = ut.string_to_timestamp(ut.arrow_to_string(format_v="YYYY-MM-DD") + ' 00:00:00')
            end = ut.string_to_timestamp(ut.arrow_to_string(format_v="YYYY-MM-DD") + ' 23:59:59')

        data["amount"] = sum([ item.amount for item in Order.objects.filter(status__in=['0','1','3'],createtime__gte=start,createtime__lte=end) ])

        return {"data":data}