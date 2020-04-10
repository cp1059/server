
from project.config_include.common import ServerUrl
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector
from app.user.serialiers import UsersSerializers
from app.user.models import Users,Role
from lib.utils.exceptions import PubErrorCustom


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
