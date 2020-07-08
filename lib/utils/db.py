
import json
from   django_redis  import   get_redis_connection
from lib.utils.exceptions import PubErrorCustom
from lib.utils.mytime import UtilTime
from lib.utils.log import logger

class RedisHandler(object):
    def __init__(self,**kwargs):
        self.redis_client = get_redis_connection(kwargs.get("db") if kwargs.get("db") else 'default') \
            if not kwargs.get('redis_client',None) else kwargs.get('redis_client',None)
        self.key = str(kwargs.get("key",None))

    def redis_dict_set(self,value):
        self.redis_client.set(self.key,json.dumps(value))

    def redis_dict_get(self):
        res = self.redis_client.get(self.key)
        return json.loads(res) if res else res

    def redis_dict_del(self):
        self.redis_client.delete(self.key)
        return None

class RedisIdGenerator(RedisHandler):

    def __init__(self,**kwargs):
        kwargs.setdefault('db','generator')
        if not kwargs.get("key",None):
            raise PubErrorCustom("key不能为空!")
        super().__init__(**kwargs)

    def run(self):
        raise PubErrorCustom("Not is func!")


class RedisIdGeneratorForCard(RedisIdGenerator):
    """
    获取充值卡卡号
    """
    def __init__(self,**kwargs):
        kwargs.setdefault('key', 'czCard')
        super().__init__(**kwargs)

    def run(self):
        return "%s%06d"%("CZ",self.redis_client.incr(self.key))


class RedisIdGeneratorForUser(RedisIdGenerator):
    """
    获取用户ID,通过传入角色ID获取值
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def run(self):
        print(self.key)
        return "%s%08d"%(self.key,self.redis_client.incr(self.key))

class RedisIdGeneratorForOrder(RedisIdGenerator):
    """
    获取订单ID
    """
    def __init__(self,**kwargs):
        t = UtilTime().arrow_to_string(format_v="YYYYMMDDHHmmss")
        kwargs.setdefault('key', t)
        super().__init__(**kwargs)

    def run(self):
        res = "TC%s%03d"%(self.key,self.redis_client.incr(self.key))
        self.redis_client.expire(self.key,10)
        return res

class RedisIdGeneratorForCpBigType(RedisIdGenerator):
    """
    获取彩票大类代码
    """
    def __init__(self,**kwargs):
        kwargs.setdefault('key', 'cpbigtypeForid')
        super().__init__(**kwargs)

    def run(self):
        return "%s%04d"%("B",self.redis_client.incr(self.key))

class RedisIdGeneratorForCpSmallType(RedisIdGenerator):
    """
    获取彩票中类代码
    """
    def __init__(self,**kwargs):
        kwargs.setdefault('key', 'cpsmalltypeForid')
        super().__init__(**kwargs)

    def run(self):
        return "%s%04d"%("S",self.redis_client.incr(self.key))

class RedisIdGeneratorForCpMiniType(RedisIdGenerator):
    """
    获取彩票小类代码
    """
    def __init__(self,**kwargs):
        kwargs.setdefault('key', 'cpminitypeForid')
        super().__init__(**kwargs)

    def run(self):
        return "%s%04d"%("M",self.redis_client.incr(self.key))

class RedisIdGeneratorForCpGamesType(RedisIdGenerator):
    """
    获取彩票玩法代码
    """
    def __init__(self,**kwargs):
        kwargs.setdefault('key', 'cpgamesForid')
        super().__init__(**kwargs)

    def run(self):
        return "%s%04d"%("G",self.redis_client.incr(self.key))

class RedisCaCheHandlerBase(RedisHandler):

    def __init__(self,**kwargs):
        kwargs.setdefault('db', 'cache')
        # if not kwargs.get("key",None):
        #     raise PubErrorCustom("key不能为空!")

        super().__init__(**kwargs)

    def redis_set(self,value):
        self.redis_client.set(self.key,json.dumps(value))

    def redis_get(self):
        res = self.redis_client.get(self.key)
        return json.loads(res) if res else res

    def redis_dict_set(self,dictKey,value):
        self.redis_client.hset(self.key,dictKey,json.dumps(value))

    def redis_dict_get(self,dictKey):
        res = self.redis_client.hget(self.key,dictKey)
        return json.loads(res) if res else res

    def redis_dict_del(self,dictKey):
        self.redis_client.hdel(self.key,dictKey)
        return None

    def redis_dict_delall(self):
        self.redis_client.delete(self.key)
        return None

    def redis_dict_get_all(self):

        res = self.redis_client.hgetall(self.key)

        res_ex={}
        if res:
            for key in res:
                res_ex[key.decode()] = json.loads(res[key])
        return res_ex if res else None

class RedisCaCheHandlerCitySheng(RedisCaCheHandlerBase):
    def __init__(self,**kwargs):
        kwargs.setdefault("key","City_Sheng")
        super().__init__(**kwargs)


class RedisCaCheHandlerCityShi(RedisCaCheHandlerBase):
    def __init__(self,**kwargs):
        kwargs.setdefault("key","City_Shi")
        super().__init__(**kwargs)

class RedisCaCheHandlerCityXian(RedisCaCheHandlerBase):
    def __init__(self,**kwargs):
        kwargs.setdefault("key","City_Xian")
        super().__init__(**kwargs)



class RedisTokenHandler(RedisHandler):
    def __init__(self,**kwargs):
        kwargs.setdefault('db', 'token')
        super().__init__(**kwargs)

class RedisAppHandler(RedisHandler):
    """
    app升级
        data:{
            "version":"100",
            "url":"",
            "note":"修改bug"
        }
    """
    def __init__(self,**kwargs):
        kwargs.setdefault('db', 'token')
        super().__init__(**kwargs)
        self.key = "sys_update_{}".format('android')

    def set(self,data=None):
        self.redis_client.set(self.key, json.dumps(data))

    def get(self):
        res = self.redis_client.get(self.key)
        return json.loads(res.decode('utf-8')) if res else res

    def isUpdate(self,version):

        res = self.get()
        logger.info("上传版本号{},系统版本{}".format(version,res))
        if res and version and int(res['version']) > int(version):
            return res
        else:
            return None

class RedisUserSysSetting(RedisHandler):
    """
    系统设置
        data:{
            ggl:""
        }
    """

    def __init__(self, **kwargs):
        kwargs.setdefault('db', 'token')
        super().__init__(**kwargs)
        self.key = "sys_setting"

    def set(self, data=None):
        self.redis_client.set(self.key, json.dumps(data))

    def get(self):
        res = self.redis_client.get(self.key)
        logger.info(res)
        return json.loads(res.decode('utf-8')) if res else {}