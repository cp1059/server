
from rest_framework import viewsets
from rest_framework.decorators import list_route
import json

from lib.utils.exceptions import PubErrorCustom
from lib.core.decorator.response import Core_connector

from app.cache.utils import RedisCaCheHandler
from lib.utils.db import RedisCaCheHandlerBase

from app.cp.models import CpTermList,Cp
from app.cp.serialiers import CpTermListModelSerializer

from app.cp.utils import count_downtime,get_open_history,get_open_term,get_rate,showdatetime

class FilterAPIView(viewsets.ViewSet):

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getHomeData(self,request):
        """
        获取首页数据
        """
        rdata={
            "banners":[],
            "cp":[]
        }

        #轮播图数据
        rdata['banners'] = [ dict(
            id = item['id'],
            url = item['url'],
            link = item['link'],
            sort = item['sort'],
            video = item['url'] if item['type'] == '1' else ""
        ) for item in RedisCaCheHandler(
            method="filter",
            serialiers="BannerModelSerializerToRedis",
            table="banner",
            filter_value={}
        ).run() ]
        rdata['banners'].sort(key=lambda k: (k.get('sort', 0)), reverse=False)

        #彩票数据
        rdata['cp'] = [ dict(
            id = item['id'],
            url = item['url'],
            name=item['name'],
            sort = item['sort'],
            termnum = "{}分钟一期".format(item['termnum'])
        ) for item in RedisCaCheHandler(
            method="filter",
            serialiers="CpModelSerializerToRedis",
            table="cp",
            filter_value={}
        ).run() ]
        rdata['cp'].sort(key=lambda k: (k.get('sort', 0)), reverse=False)

        return {"data":rdata}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getPlayingData(self,request):
        """
        获取开奖数据
        :param request:
        :return:
        """

        data = CpTermListModelSerializer(CpTermList.objects.filter(),many=True).data

        # def updtimeshow(s):
        #     s['createtime'] = showdatetime(s['createtime'])
        #     return s
        # data = list(map( updtimeshow, [ dict(item) for item in data ]))
        # print(data)
        data =  [ dict(item) for item in data ]
        data.sort(key=lambda k: (k.get('cp').get('sort',0)), reverse=False)

        return {"data":data}


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getBuyData(self,request):
        # redis_cli_ctypes = RedisCaCheHandlerBase(db="default",key="cptypes")
        # res = [ value for key, value in redis_cli_ctypes.redis_dict_get_all().items() ]
        # res.sort(key=lambda k: (k.get('id', 0)), reverse=False)

        res = RedisCaCheHandler(
            method="filter",
            serialiers="CpBigTypeModelSerializerToRedis",
            table="cpbigtype",
            filter_value={}
        ).run()
        res.sort(key=lambda k: (k.get('id', 0)), reverse=False)

        return {"data":res}


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getBuyDataForList(self,request):

        if not request.query_params_format.get("id",None):
            raise PubErrorCustom("传入彩票分类ID有误!")

        RCaCheClass = RedisCaCheHandler()
        RCaCheClass.customInit(
            method="filter",
            serialiers="CpModelSerializerToRedis",
            table="cp",
            filter_value={"cptypeid": request.query_params_format.get("id", None)}
        )
        res = []

        for r in RCaCheClass.run():

            cpObj = {
                "id": r.get("id",None),
                "name": r.get("name", None),
                "sort": r.get("sort", None),
                "url": r.get("url", None),
                "cptypeid": r.get("cptypeid", None),
                "typename": r.get("typename", None),
                "status": r.get("status", None)
            }

            res.append(cpObj)

        res.sort(key=lambda k: (k.get('sort', 0)), reverse=False)

        return {"data":res}


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getCpData(self,request):

        if not request.query_params_format.get("id",None):
            raise PubErrorCustom("传入彩票ID有误!")

        RCaCheClass = RedisCaCheHandler()
        RCaCheClass.customInit(
            method="get",
            serialiers="CpModelSerializerToRedis",
            table="cp",
            must_key_value=request.query_params_format.get("id",None)
        )
        cpObj = RCaCheClass.run()

        RCaCheClassSmallType = RedisCaCheHandler()
        RCaCheClassMiniType = RedisCaCheHandler()
        RCaCheClassGames = RedisCaCheHandler()

        RCaCheClassSmallType.customInit(
            method="filter",
            serialiers="CpSmallTypeModelSerializerToRedis",
            table="cpsmalltype",
            filter_value={"bigtypeid": cpObj['cptypeid']}
        )

        cpObj['smalltype'] = RCaCheClassSmallType.run()
        cpObj['smalltype'].sort(key=lambda k: (k.get('sort', 0)), reverse=False)

        for smalltype in cpObj['smalltype']:

            RCaCheClassMiniType.customInit(
                method="filter",
                serialiers="CpMiniTypeModelSerializerToRedis",
                table="cpminitype",
                filter_value={"smalltypeid": smalltype['typeid'], "bigtypeid": cpObj['cptypeid']}
            )

            smalltype['minitype'] = RCaCheClassMiniType.run()
            smalltype['minitype'].sort(key=lambda k: (k.get('sort', 0)), reverse=False)

            for minitype in smalltype['minitype']:
                RCaCheClassGames.customInit(
                    method="filter",
                    serialiers="CpGamesModelSerializerToRedis",
                    table="cpgames",
                    filter_value={"minitypeid": minitype['typeid'], "smalltypeid": smalltype['typeid'],
                                  "bigtypeid": cpObj['cptypeid']}
                )

                minitype['games'] = RCaCheClassGames.run()
                minitype['games'].sort(key=lambda k: (k.get('sort', 0)), reverse=False)


                for item in minitype['games']:
                    item['rules']['rate'] = get_rate(item['rules'])

        cpObj['cpnohistory'] = get_open_history(cpObj)
        cpObj['downterm'],cpObj['downtime'] = count_downtime(cpObj)

        return {"data": {
            "id":cpObj['id'],
            "url":cpObj['url'],
            "name":cpObj['name'],
            "downtime":cpObj['downtime'],
            "cpnohistory":cpObj['cpnohistory'],
            "downterm":cpObj['downterm'],
            "smalltype":cpObj['smalltype']
        }}


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getVideo(self,request):

        videos = [ dict(
            id = item['id'],
            url = item['url'],
            sort = item['sort']
        ) for item in RedisCaCheHandler(
            method="filter",
            serialiers="VideoModelSerializerToRedis",
            table="video",
            filter_value={}
        ).run() ]
        videos.sort(key=lambda k: (k.get('sort', 0)), reverse=False)

        return {"data":videos}