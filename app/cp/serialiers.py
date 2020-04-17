


from rest_framework import serializers
from app.cp.models import Cp,CpTermList,CpBigType,CpSmallType,CpMiniType,CpGames
from app.cache.utils import RedisCaCheHandler

from lib.utils.mytime import UtilTime
from app.cp.utils import showdatetime


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

        return showdatetime(obj.createtime)


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