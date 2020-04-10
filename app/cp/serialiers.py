


from rest_framework import serializers
from app.cp.models import Cp,CpTermList,CpBigType,CpSmallType,CpMiniType,CpGames
from app.cache.utils import RedisCaCheHandler

from lib.utils.mytime import UtilTime


class CpModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cp
        fields = '__all__'

class CpTermListModelSerializer(serializers.ModelSerializer):


    cp = serializers.SerializerMethodField()
    showtime = serializers.SerializerMethodField()
    showno = serializers.SerializerMethodField()


    def get_showno(self,obj):

        return [ item for item in obj.cpno.split(",") ]


    def get_showtime(self,obj):

        t = UtilTime().timestamp_to_string(obj.createtime,format_v="%Y%m%d %H:%M:%S")

        t1 = t[:8]
        t2 = UtilTime().arrow_to_string(format_v="YYYYMMDD")

        r=""
        if int(t2) - int(t1)==0:
            r="今天"
        elif int(t2) - int(t1)==1:
            r="昨天"
        else:
            r="未知"

        return "{}{}".format(r,t[8:])


    def get_cp(self,obj):
        r = RedisCaCheHandler(
            method="get",
            serialiers="CpModelSerializerToRedis",
            table="cp",
            must_key_value=obj.cpid
        ).run()

        return {
            "name" : r.get("name",None),
            "sort": r.get("sort",None),
            "url": r.get("url", None),
            "cptypeid": r.get("cptypeid", None),
            "typename": r.get("typename", None),
            "status": r.get("status", None)
        }

    class Meta:
        model = CpTermList
        fields = '__all__'

class CpBigTypeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CpBigType
        fields = '__all__'

class CpSmallTypeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CpSmallType
        fields = '__all__'

class CpMiniTypeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CpMiniType
        fields = '__all__'

class CpGamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CpGames
        fields = '__all__'