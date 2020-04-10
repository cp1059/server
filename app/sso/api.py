
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector
from lib.utils.exceptions import PubErrorCustom
from lib.utils.db import RedisTokenHandler
from lib.utils.string_extension import get_token
from app.idGenerator import idGenerator

from app.user.models import Users
from app.cache.serialiers import UserModelSerializerToRedis

class SsoAPIView(viewsets.ViewSet):

    @list_route(methods=['POST'])
    @Core_connector(isPasswd=True,isTransaction=True)
    def register(self, request):

        """
        普通玩家注册
        :param request:
        :return:
        """

        if Users.objects.filter(loginname=request.data_format.get('loginname')).count():
            raise PubErrorCustom("该账号已存在!")

        user = Users.objects.create(**{
            "userid":idGenerator.userid("2001"),
            "name": request.data_format.get("loginname",""),
            "loginname":request.data_format.get("loginname",""),
            "passwd": request.data_format.get("password", ""),
            "mobile": request.data_format.get("mobile", ""),
            "code": request.data_format.get("code", ""),
            "rolecode":"2001"
        })
        token = get_token()
        res = UserModelSerializerToRedis(user, many=False).data
        RedisTokenHandler(key=token).redis_dict_set(res)

        return {"data": {
            "token": token,
            "userinfo": {
                "rolecode": user.rolecode
            }
        }}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True)
    def login(self, request):

        try:
            user = Users.objects.get(loginname=request.data_format.get('loginname'),rolecode__in=['1000','1001'])
        except Users.DoesNotExist:
            raise PubErrorCustom("登录账号或密码错误！")

        if user.passwd != self.request.data_format.get('password'):
            raise PubErrorCustom("登录账号或密码错误！")

        if user.status == 1:
            raise PubErrorCustom("登陆账号已到期！")
        elif user.status == 2:
            raise PubErrorCustom("已冻结！")
        token = get_token()
        res = UserModelSerializerToRedis(user, many=False).data
        RedisTokenHandler(key=token).redis_dict_set(res)

        return {"data": {
            "token": token
        }}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isPasswd=True)
    def login1(self, request):
        """
        普通玩家
        :param request:
        :return:
        """
        try:
            user = Users.objects.get(loginname=request.data_format.get('loginname'), rolecode__in=['2001'])
        except Users.DoesNotExist:
            raise PubErrorCustom("登录账号或密码错误！")

        if user.passwd != self.request.data_format.get('password'):
            raise PubErrorCustom("登录账号或密码错误！")

        if user.status == 1:
            raise PubErrorCustom("登陆账号已到期！")
        elif user.status == 2:
            raise PubErrorCustom("已冻结！")
        token = get_token()
        res = UserModelSerializerToRedis(user, many=False).data
        RedisTokenHandler(key=token).redis_dict_set(res)

        return {"data": {
            "token": token,
            "userinfo":{
                "rolecode":user.rolecode
            }
        }}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isPasswd=True)
    def login2(self, request):
        """
        试玩玩家
        :param request:
        :return:
        """
        user = Users.objects.create(**{
            "userid": idGenerator.userid("2002"),
            "rolecode": "2002",
            "bal":1000.0
        })
        user.name = user.userid
        user.loginname = user.userid
        user.save()

        token = get_token()
        res = UserModelSerializerToRedis(user, many=False).data
        RedisTokenHandler(key=token).redis_dict_set(res)

        return {"data": {
            "token": token,
            "userinfo":{
                "rolecode":user.rolecode
            }
        }}

    #登出
    @list_route(methods=['POST'])
    @Core_connector(isPasswd=True,isTicket=True)
    def logout(self,request, *args, **kwargs):

        RedisTokenHandler(key=request.ticket).redis_dict_del()
        return None

    #刷新token
    @list_route(methods=['POST'])
    @Core_connector(isPasswd=True,isTicket=True)
    def refeshToken(self,request, *args, **kwargs):

        redis_cli = RedisTokenHandler(key=request.ticket)
        res = redis_cli.redis_dict_get()
        redis_cli.redis_dict_del()

        token = get_token()
        redis_cli = RedisTokenHandler(key=token)
        redis_cli.redis_dict_set(res)

        return { "data": token}