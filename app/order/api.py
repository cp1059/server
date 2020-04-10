
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

class OrderAPIView(viewsets.ViewSet):


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
                serialiers="CpGamesModelSerializerToRedis",
                table="cpgames",
                must_key_value=cp['gamesid']
            )
            games = RCaCheClassGames.run()
            if not games:
                raise PubErrorCustom("无此玩法!")

            rate = ""
            if games['rules']['ratetype'] == '0':
                rate = games['rules']['rate']

            Order.objects.create(**{
                "userid":request.user['userid'],
                "amount":curramount,
                "num":cp['num'],
                "term":get_next_term(cp['cpid']),
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
            WHERE 1=1 %s order by t1.createtime %s
        """% (query_format,limit_format), query_params)

        return { "data" : OrderSerializer(orders,many=True).data }

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