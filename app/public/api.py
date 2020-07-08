from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector
from lib.utils.db import RedisCaCheHandlerBase

from include.game import cptypes

from app.public.menu import all_menu

from app.cp.models import Cp,CpBigType,CpSmallType,CpMiniType,CpGames

from app.cache.utils import RedisCaCheHandler


from app.public.serialiers import BannerModelSerializer,VideoModelSerializer,HolidayModelSerializer
from app.public.models import Banner,Video,Holiday

from lib.utils.db import RedisAppHandler,RedisUserSysSetting
from lib.utils.exceptions import PubErrorCustom

class PublicAPIView(viewsets.ViewSet):


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getMenu(self, request):
        """
        获取菜单数据
        :param request:
        :return:
        """

        type = self.request.query_params.get('type') if self.request.query_params.get("type") else "first"
        return {"data":all_menu[type]}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getTopMenu(self, request):
        """
        获取顶部菜单数据
        :param request:
        :return:
        """

        return {"data":all_menu['top']}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isPasswd=True)
    def init_project(self, request):

        """
        初始化项目
        :param request:
        :return:
        """

        ##初始化彩票分类以及玩法数据
        redis_cli_ctypes = RedisCaCheHandlerBase(db="default",key="cptypes")

        for item in cptypes:
            redis_cli_ctypes.redis_dict_set(item['id'],{"name":item['name'],"id":item['id']})

            redis_cli_biggametype = RedisCaCheHandlerBase(db="default", key="biggametype_{}".format(item['id']))

            for item_biggametype in item['value']:
                redis_cli_biggametype.redis_dict_set(item_biggametype['id'], {"name": item_biggametype['name'], "id": item_biggametype['id']})

                redis_cli_smallgametype = RedisCaCheHandlerBase(db="default", key="smallgametype_{}".format(item_biggametype['id']))

                for item_smallgametype in item_biggametype['value']:
                    redis_cli_smallgametype.redis_dict_set(item_smallgametype['id'], {"name": item_smallgametype['name'], "id": item_smallgametype['id']})

                    redis_cli_minigametype = RedisCaCheHandlerBase(db="default",
                                                               key="minigametype_{}".format(item_smallgametype['id']))

                    for item_minigametype in item_smallgametype['value']:

                        redis_cli_minigametype.redis_dict_set(item_minigametype['id'],item_minigametype)


        return None

    #刷新所有缓存数据
    @list_route(methods=['POST'])
    @Core_connector()
    def refeshCacheForRedis(self,request):

        RedisCaCheHandler(
            method="saveAll",
            serialiers="CpModelSerializerToRedis",
            table="cp",
            filter_value=Cp.objects.filter(),
            must_key="id",
        ).run()

        RedisCaCheHandler(
            method="saveAll",
            serialiers="CpBigTypeModelSerializerToRedis",
            table="cpbigtype",
            filter_value=CpBigType.objects.filter(),
            must_key="typeid",
        ).run()

        RedisCaCheHandler(
            method="saveAll",
            serialiers="CpSmallTypeModelSerializerToRedis",
            table="cpsmalltype",
            filter_value=CpSmallType.objects.filter(),
            must_key="typeid",
        ).run()

        RedisCaCheHandler(
            method="saveAll",
            serialiers="CpMiniTypeModelSerializerToRedis",
            table="cpminitype",
            filter_value=CpMiniType.objects.filter(),
            must_key="typeid",
        ).run()

        RedisCaCheHandler(
            method="saveAll",
            serialiers="CpGamesModelSerializerToRedis",
            table="cpgames",
            filter_value=CpGames.objects.filter(),
            must_key="typeid",
        ).run()

        RedisCaCheHandler(
            method="saveAll",
            serialiers="BannerModelSerializerToRedis",
            table="banner",
            filter_value=Banner.objects.filter(),
            must_key="id",
        ).run()

        RedisCaCheHandler(
            method="saveAll",
            serialiers="VideoModelSerializerToRedis",
            table="video",
            filter_value=Video.objects.filter(),
            must_key="id",
        ).run()

        return None

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True,
                    serializer_class=BannerModelSerializer,
                    model_class=Banner)
    def saveBanner(self, request, *args, **kwargs):

        serializer = kwargs.pop("serializer")
        obj = serializer.save()

        RedisCaCheHandler(
            method="save",
            serialiers="BannerModelSerializerToRedis",
            table="banner",
            filter_value=obj,
            must_key="id",
        ).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True, isPagination=True)
    def getBanner(self, request, *args, **kwargs):

        obj = RedisCaCheHandler(
            method="filter",
            serialiers="BannerModelSerializerToRedis",
            table="banner"
        ).run()
        return {"data": obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isTicket=True, isPasswd=True)
    def delBanner(self, request, *args, **kwargs):

        Banner.objects.filter(id=request.data_format.get('id')).delete()

        RedisCaCheHandler(
            method="delete",
            table="banner",
            must_key_value=request.data_format.get('id')).run()

        return None

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True,
                    serializer_class=VideoModelSerializer,
                    model_class=Video)
    def saveVideo(self, request, *args, **kwargs):

        serializer = kwargs.pop("serializer")
        obj = serializer.save()

        RedisCaCheHandler(
            method="save",
            serialiers="VideoModelSerializerToRedis",
            table="video",
            filter_value=obj,
            must_key="id",
        ).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True, isPagination=True)
    def getVideo(self, request, *args, **kwargs):

        obj = RedisCaCheHandler(
            method="filter",
            serialiers="VideoModelSerializerToRedis",
            table="video"
        ).run()

        return {"data": obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isTicket=True, isPasswd=True)
    def delVideo(self, request, *args, **kwargs):

        Video.objects.filter(id=request.data_format.get('id')).delete()

        RedisCaCheHandler(
            method="delete",
            table="video",
            must_key_value=request.data_format.get('id')).run()

        return None


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True,
                    serializer_class=HolidayModelSerializer,
                    model_class=Holiday)
    def saveHoliday(self, request, *args, **kwargs):

        serializer = kwargs.pop("serializer")
        obj = serializer.save()

        RedisCaCheHandler(
            method="save",
            serialiers="HolidayModelSerializerToRedis",
            table="holiday",
            filter_value=obj,
            must_key="id",
        ).run()

        return None


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isTicket=True, isPasswd=True)
    def delHoliday(self, request, *args, **kwargs):

        Holiday.objects.filter(id=request.data_format.get('id')).delete()

        RedisCaCheHandler(
            method="delete",
            table="holiday",
            must_key_value=request.data_format.get('id')).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True, isPagination=True)
    def getHoliday(self, request, *args, **kwargs):

        obj = RedisCaCheHandler(
            method="filter",
            serialiers="HolidayModelSerializerToRedis",
            table="holiday"
        ).run()

        return {"data": obj}


    @list_route(methods=['POST'])
    @Core_connector(isPasswd=True)
    def appUpdate(self, request):

        version = request.data_format.get("version",None)
        url =  request.data_format.get("url",None)
        note = request.data_format.get("note", None)

        if not version:
            raise PubErrorCustom("版本号不能为空")

        if not url:
            raise PubErrorCustom("下载地址不能为空!")

        if not note:
            raise PubErrorCustom("更新内容不能为空!")

        RedisAppHandler().set(data={
            "version":version,
            "url":url,
            "note":note
        })

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def appGet(self, request):

        return {"data":RedisAppHandler().get()}

    @list_route(methods=['POST'])
    @Core_connector(isPasswd=True)
    def sysSettingUpdate(self, request):

        ggl = request.data_format.get("ggl", None)

        if not ggl:
            raise PubErrorCustom("公告栏消息不能为空!")

        RedisUserSysSetting().set(data={
            "ggl": ggl
        })

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def sysSettingGet(self, request):
        res = RedisUserSysSetting().get()
        print(res)

        return {"data":res}