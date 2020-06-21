
import json
from rest_framework import serializers
from app.user.models import Users,Role
from lib.utils.mytime import UtilTime

class RoleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'

class UsersSerializers(serializers.Serializer):

    bal = serializers.DecimalField(max_digits=16, decimal_places=3)
    name = serializers.CharField()

class UsersModelSerializer(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()
    bal = serializers.DecimalField(max_digits=16, decimal_places=2)
    status_format = serializers.SerializerMethodField()

    rolename = serializers.SerializerMethodField()


    def get_rolename(self,obj):
        try:
            roleObj = Role.objects.get(rolecode=obj.rolecode)
            return roleObj.name
        except Role.DoesNotExist:
            return "未知"

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    def get_status_format(self,obj):

        if obj.status == '0':
            return "正常"
        elif obj.status == '1':
            return "到期"
        else:
            return "冻结"

    class Meta:
        model = Users
        fields = '__all__'