
from project.config_include.common import ServerUrl
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector
from app.user.serialiers import UsersSerializers,UsersModelSerializer
from app.user.models import Users,Role
from lib.utils.exceptions import PubErrorCustom
from lib.utils.mytime import UtilTime
from decimal import Decimal

class UserAPIView(viewsets.ViewSet):


    @list_route(methods=['GET'])
    @Core_connector(isTicket=True,isPasswd=True)
    def getUserInfo(self, request):

        return {"data": {
            "userInfo": {
                "username": request.user.get("uuid"),
                "name": request.user.get("name"),
                'rolecode': request.user.get("role").get("rolecode"),
                "rolename": request.user.get("role").get("rolename"),
                "avatar": ServerUrl+'/statics/images/pic.jpg',
                'roles': [ {"name":item.name,"rolecode":item.rolecode} for item in Role.objects.filter(rolecode__startswith='4')]
            },
            "roles": request.user.get("role").get("rolecode"),
            "permission": []
        }}


    @list_route(methods=['GET'])
    @Core_connector(isTicket=True,isPasswd=True)
    def getUser(self, request):
        try:
            user = Users.objects.get(userid=request.user['userid'])
            if user.status !='0':
                raise PubErrorCustom("用户状态异常!")
        except Users.DoesNotExist:
            raise PubErrorCustom("用户不存在!")

        return {"data":UsersSerializers(user,many=False).data}

    @list_route(methods=['GET'])
    @Core_connector(isTicket=True,isPasswd=True,isPagination=True)
    def getUserByWeb(self, request):

        rolecode = request.query_params_format.get("rolecode")
        startdate = request.query_params_format.get("startdate")
        enddate = request.query_params_format.get("enddate")
        status = request.query_params_format.get("status")

        ut = UtilTime()

        user = Users.objects.filter(rolecode__startswith=2)

        if status:
            user = user.filter(status=status)

        if startdate and enddate:
            user = user.filter(createtime__gte=ut.string_to_timestamp(startdate),createtime__lte=ut.string_to_timestamp(enddate))

        if rolecode:
            user = user.filter(rolecode=rolecode)

        return {"data":UsersModelSerializer(user.order_by('-createtime'),many=True).data}


    @list_route(methods=['POST'])
    @Core_connector(isTicket=True,isPasswd=True,isTransaction=True)
    def UserStop(self, request):

        Users.objects.filter(userid__in=request.data_format.get("userids",[])).update(status='2')

    @list_route(methods=['POST'])
    @Core_connector(isTicket=True,isPasswd=True,isTransaction=True)
    def UserUpdBal(self, request):

        amount = request.data_format.get("amount")

        if not amount:
            raise PubErrorCustom("修改金额不能为空!")

        for item in Users.objects.select_for_update().filter(userid__in=request.data_format.get("userids",[])):
            item.bal += Decimal(str(amount))
            item.save()