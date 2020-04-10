
from lib.utils.db import RedisIdGeneratorForOrder,RedisIdGeneratorForUser,RedisIdGeneratorForCpBigType,\
                RedisIdGeneratorForCpSmallType,RedisIdGeneratorForCpMiniType,RedisIdGeneratorForCpGamesType
class idGenerator(object):

    def __init__(self):
        pass

    @staticmethod
    def userid(rolecode):
        return RedisIdGeneratorForUser(key=rolecode).run()

    @staticmethod
    def ordercode():
        return RedisIdGeneratorForOrder().run()

    @staticmethod
    def cpbigtype():
        return RedisIdGeneratorForCpBigType().run()

    @staticmethod
    def cpsmalltype():
        return RedisIdGeneratorForCpSmallType().run()

    @staticmethod
    def cpminitype():
        return RedisIdGeneratorForCpMiniType().run()

    @staticmethod
    def cpgames():
        return RedisIdGeneratorForCpGamesType().run()

