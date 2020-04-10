
import re,json
from requests import request as requestTmp

from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector
from lib.utils.db import RedisCaCheHandlerBase

from lib.utils.exceptions import PubErrorCustom

from app.cache.utils import RedisCaCheHandler
from app.cp.models import Cp,CpGames,CpMiniType,CpSmallType,CpBigType
from app.cp.serialiers import CpModelSerializer,\
    CpGamesModelSerializer,CpBigTypeModelSerializer,CpMiniTypeModelSerializer,\
            CpSmallTypeModelSerializer

from app.cp.utils import countTotTerm,create_task_table


class CpAPIView(viewsets.ViewSet):


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getCpTypes(self, request):

        redis_cli_ctypes = RedisCaCheHandlerBase(db="default",key="cptypes")
        res = redis_cli_ctypes.redis_dict_get_all()
        return {"data":res}


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getCpBigGameType(self, request):

        if not request.query_params_format.get("cptypeid", None):
            raise PubErrorCustom("请选择彩票分类!")

        redis_cli_biggametype = RedisCaCheHandlerBase(db="default",key="biggametype_{}".format(request.query_params_format.get("cptypeid", None)))

        res = redis_cli_biggametype.redis_dict_get_all()

        return {"data":res}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getCpSmallGameType(self, request):

        if not request.query_params_format.get("cpbiggametypeid", None):
            raise PubErrorCustom("请选择彩票玩法大类!")

        redis_cli_smallgametype = RedisCaCheHandlerBase(db="default",key="smallgametype_{}".format(request.query_params_format.get("cpbiggametypeid", None)))

        res = redis_cli_smallgametype.redis_dict_get_all()

        return {"data":res}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getCpMiniGameType(self, request):

        if not request.query_params_format.get("cpsmallgametypeid", None):
            raise PubErrorCustom("请选择彩票玩法中类!")

        redis_cli_minigametype = RedisCaCheHandlerBase(db="default",key="minigametype_{}".format(request.query_params_format.get("cpsmallgametypeid", None)))

        res = redis_cli_minigametype.redis_dict_get_all()

        return {"data":res}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getCpMiniGameTypeData(self, request):

        if not request.query_params_format.get("id", None):
            raise PubErrorCustom("请选择彩票玩法子类!")

        redis_cli_minigametype = RedisCaCheHandlerBase(db="default",key="minigametype_{}".format(request.query_params_format.get("id", None)[:8]))

        res = redis_cli_minigametype.redis_dict_get(request.query_params_format.get("id", None))

        return {"data":res}

    @list_route(methods=['POST'])
    @Core_connector(isPasswd=True,isTicket=True)
    def updCpMiniGameTypeData(self, request):

        if not request.data_format.get("id", None):
            raise PubErrorCustom("请选择彩票玩法子类!")

        if not request.data_format.get("form", None):
            raise PubErrorCustom("提交数据为空!")

        redis_cli_minigametype = RedisCaCheHandlerBase(db="default",key="minigametype_{}".format(request.data_format.get("id", None)[:8]))

        redis_cli_minigametype.redis_dict_set(request.data_format.get("id", None),request.data_format.get("form", None))

        return {"data":request.data_format.get("form", None)}

    @list_route(methods=['POST'])
    @Core_connector(isPasswd=True,
                    isTicket=True)
    def cpGetTest(self,request):
        code = self.request.data_format.get("code")
        context={}
        exec(code,context)
        res = context["customFuncForCp"]
        res = res(requestTmp,re,json)
        try:
            return {"data": "测试成功\n数据为(当前期:{}  当前开奖号:{}  下一期:{})".format(res[0],res[1],res[2])}
        except Exception as e:
            return {"data":str(e)}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True,
                    serializer_class=CpModelSerializer,
                    model_class=Cp)
    def saveCp(self, request, *args, **kwargs):

        serializer = kwargs.pop("serializer")
        obj = serializer.save()

        obj.termtot = countTotTerm(obj.opentime,obj.termnum)
        obj.tasktimetable = json.dumps({"tables":create_task_table(obj)})
        obj.save()

        RedisCaCheHandler(
            method="save",
            serialiers="CpModelSerializerToRedis",
            table="cp",
            filter_value=obj,
            must_key="id",
        ).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True, isPagination=True)
    def getCp(self, request, *args, **kwargs):

        obj = RedisCaCheHandler(
            method="filter",
            serialiers="CpModelSerializerToRedis",
            table="cp",
            filter_value=request.query_params_format
        ).run()

        return {"data": obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isTicket=True, isPasswd=True)
    def delCp(self, request, *args, **kwargs):


        Cp.objects.filter(id=request.data_format.get('id')).delete()

        RedisCaCheHandler(
            method="delete",
            table="cp",
            must_key_value=request.data_format.get('id')).run()

        return None



    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True,
                    serializer_class=CpBigTypeModelSerializer,
                    model_class=CpBigType)
    def saveCpBigType(self, request, *args, **kwargs):

        serializer = kwargs.pop("serializer")
        obj = serializer.save()

        RedisCaCheHandler(
            method="save",
            serialiers="CpBigTypeModelSerializerToRedis",
            table="cpbigtype",
            filter_value=obj,
            must_key="typeid",
        ).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True, isPagination=True)
    def getCpBigType(self, request, *args, **kwargs):

        obj = RedisCaCheHandler(
            method="filter",
            serialiers="CpBigTypeModelSerializerToRedis",
            table="cpbigtype",
            filter_value=request.query_params_format
        ).run()

        return {"data": obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isTicket=True, isPasswd=True)
    def delCpBigType(self, request, *args, **kwargs):

        CpBigType.objects.filter(typeid=request.data_format.get('typeid')).delete()

        RedisCaCheHandler(
            method="delete",
            table="cpbigtype",
            must_key_value=request.data_format.get('typeid')).run()

        return None



    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True,
                    serializer_class=CpSmallTypeModelSerializer,
                    model_class=CpSmallType)
    def saveCpSmallType(self, request, *args, **kwargs):

        serializer = kwargs.pop("serializer")
        obj = serializer.save()

        RedisCaCheHandler(
            method="save",
            serialiers="CpSmallTypeModelSerializerToRedis",
            table="cpsmalltype",
            filter_value=obj,
            must_key="typeid",
        ).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True, isPagination=True)
    def getCpSmallType(self, request, *args, **kwargs):

        obj = RedisCaCheHandler(
            method="filter",
            serialiers="CpSmallTypeModelSerializerToRedis",
            table="cpsmalltype",
            filter_value=request.query_params_format
        ).run()

        return {"data": obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isTicket=True, isPasswd=True)
    def delCpSmallType(self, request, *args, **kwargs):

        CpSmallType.objects.filter(typeid=request.data_format.get('typeid')).delete()

        RedisCaCheHandler(
            method="delete",
            table="cpsmalltype",
            must_key_value=request.data_format.get('typeid')).run()

        return None

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True,
                    serializer_class=CpMiniTypeModelSerializer,
                    model_class=CpMiniType)
    def saveCpMiniType(self, request, *args, **kwargs):

        serializer = kwargs.pop("serializer")
        obj = serializer.save()

        RedisCaCheHandler(
            method="save",
            serialiers="CpMiniTypeModelSerializerToRedis",
            table="cpminitype",
            filter_value=obj,
            must_key="typeid",
        ).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True, isPagination=True)
    def getCpMiniType(self, request, *args, **kwargs):

        obj = RedisCaCheHandler(
            method="filter",
            serialiers="CpMiniTypeModelSerializerToRedis",
            table="cpminitype",
            filter_value=request.query_params_format
        ).run()

        return {"data": obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isTicket=True, isPasswd=True)
    def delCpMiniType(self, request, *args, **kwargs):

        CpMiniType.objects.filter(typeid=request.data_format.get('typeid')).delete()

        RedisCaCheHandler(
            method="delete",
            table="cpminitype",
            must_key_value=request.data_format.get('typeid')).run()

        return None

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True,
                    serializer_class=CpGamesModelSerializer,
                    model_class=CpGames)
    def saveCpGames(self, request, *args, **kwargs):

        serializer = kwargs.pop("serializer")
        obj = serializer.save()

        RedisCaCheHandler(
            method="save",
            serialiers="CpGamesModelSerializerToRedis",
            table="cpgames",
            filter_value=obj,
            must_key="typeid",
        ).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True, isPagination=True)
    def getCpGames(self, request, *args, **kwargs):

        obj = RedisCaCheHandler(
            method="filter",
            serialiers="CpGamesModelSerializerToRedis",
            table="cpgames",
            filter_value=request.query_params_format
        ).run()

        return {"data": obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isTicket=True, isPasswd=True)
    def delCpGames(self, request, *args, **kwargs):

        CpGames.objects.filter(typeid=request.data_format.get('typeid')).delete()

        RedisCaCheHandler(
            method="delete",
            table="cpgames",
            must_key_value=request.data_format.get('typeid')).run()

        return None