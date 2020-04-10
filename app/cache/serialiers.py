
import json
from rest_framework import serializers

from lib.utils.mytime import UtilTime
from lib.utils.exceptions import PubErrorCustom
from app.user.models import Users,Role
from app.public.models import Banner,Video

from app.cp.models import Cp,CpBigType,CpSmallType,CpMiniType,CpGames


class UserModelSerializerToRedis(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()
    createtime_format = serializers.SerializerMethodField()
    bal = serializers.SerializerMethodField()

    def get_role(self,obj):
        try:
            roleObj = Role.objects.get(rolecode=obj.rolecode)
            return RoleModelSerializerToRedis(roleObj,many=False).data
        except Role.DoesNotExist:
            raise PubErrorCustom("无此角色信息!")

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    def get_bal(self,obj):
        return round(float(obj.bal),2)

    class Meta:
        model = Users
        fields = '__all__'


class RoleModelSerializerToRedis(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class CpModelSerializerToRedis(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()
    status_format = serializers.SerializerMethodField()
    type_format = serializers.SerializerMethodField()

    code = serializers.SerializerMethodField()

    cpnorule = serializers.SerializerMethodField()

    def get_cpnorule(self,obj):
        r = json.loads(obj.cpnorule)
        if len(r):
            limit = ""
            for item in r['limit']:
                limit += "{},".format(item)
            r['limit'] = limit[:-1]
            return r
        else:
            return {}

    def get_code(self,obj):

        return json.loads(obj.code)

    def get_type_format(self,obj):

        return "官方" if obj.type == '0' else '私有'

    def get_status_format(self,obj):
        if obj.status == '0':
            return "正常"
        elif obj.status=='1':
            return "停售"
        else:
            return "维护"

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = Cp
        fields = '__all__'


class BannerModelSerializerToRedis(serializers.ModelSerializer):
    createtime_format = serializers.SerializerMethodField()
    type_format = serializers.SerializerMethodField()


    def get_type_format(self, obj):

        return "图片" if obj.type == '0' else '视频'

    def get_createtime_format(self, obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = Banner
        fields = '__all__'

class VideoModelSerializerToRedis(serializers.ModelSerializer):
    createtime_format = serializers.SerializerMethodField()

    def get_createtime_format(self, obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = Video
        fields = '__all__'


class CpBigTypeModelSerializerToRedis(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()

    def get_createtime_format(self, obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = CpBigType
        fields = '__all__'

class CpSmallTypeModelSerializerToRedis(serializers.ModelSerializer):
    createtime_format = serializers.SerializerMethodField()
    bigtypename = serializers.SerializerMethodField()

    def get_createtime_format(self, obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    def get_bigtypename(self,obj):

        try:
            return CpBigType.objects.get(typeid=obj.bigtypeid).name
        except CpBigType.DoesNotExist:
            return ""

    class Meta:
        model = CpSmallType
        fields = '__all__'

class CpMiniTypeModelSerializerToRedis(serializers.ModelSerializer):
    createtime_format = serializers.SerializerMethodField()
    bigtypename = serializers.SerializerMethodField()
    smalltypename = serializers.SerializerMethodField()

    def get_createtime_format(self, obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    def get_bigtypename(self,obj):

        try:
            return CpBigType.objects.get(typeid=obj.bigtypeid).name
        except CpBigType.DoesNotExist:
            return ""

    def get_smalltypename(self,obj):

        try:
            return CpSmallType.objects.get(typeid=obj.smalltypeid).name
        except CpSmallType.DoesNotExist:
            return ""

    class Meta:
        model = CpMiniType
        fields = '__all__'

class CpGamesModelSerializerToRedis(serializers.ModelSerializer):
    createtime_format = serializers.SerializerMethodField()

    bigtypename = serializers.SerializerMethodField()
    smalltypename = serializers.SerializerMethodField()
    minitypename = serializers.SerializerMethodField()
    rules = serializers.SerializerMethodField()

    def get_rules(self,obj):

        return json.loads(obj.rules)

    def get_bigtypename(self,obj):

        try:
            return CpBigType.objects.get(typeid=obj.bigtypeid).name
        except CpBigType.DoesNotExist:
            return ""

    def get_smalltypename(self,obj):

        try:
            return CpSmallType.objects.get(typeid=obj.smalltypeid).name
        except CpSmallType.DoesNotExist:
            return ""

    def get_minitypename(self,obj):
        try:
            return CpMiniType.objects.get(typeid=obj.minitypeid).name
        except CpMiniType.DoesNotExist:
            return ""


    def get_createtime_format(self, obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = CpGames
        fields = '__all__'