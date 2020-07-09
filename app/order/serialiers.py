
import json
from rest_framework import serializers
from app.order.models import Order
from lib.utils.mytime import UtilTime

class OrderSerializer(serializers.Serializer):

    cpname = serializers.CharField()
    cpurl = serializers.CharField()
    id = serializers.IntegerField()
    userid = serializers.IntegerField()
    cpid = serializers.CharField()
    amount = serializers.DecimalField(max_digits=18,decimal_places=3)
    num = serializers.CharField()
    fd = serializers.DecimalField(max_digits=18,decimal_places=3)
    rate = serializers.CharField()
    term = serializers.CharField()
    status = serializers.SerializerMethodField()
    no = serializers.SerializerMethodField()
    orderid = serializers.CharField()
    createtime = serializers.SerializerMethodField()
    gamename = serializers.CharField()
    minitypename = serializers.CharField()

    no_format = serializers.SerializerMethodField()

    def get_no_format(self,obj):
        s=""
        for item in json.loads(obj.no)['no']:
            for cp in item['cp']:
                s+="{},".format(cp)
            s=s[:-1]
            s+="|"
        return s[:-1]

    def get_createtime(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    def get_no(self,obj):
        return json.loads(obj.no)['no']

    def get_status(self,obj):
        if obj.status == '0':
            return "待开奖"
        elif obj.status == '1':
            return "已中奖"
        elif obj.status == '2':
            return "已撤单"
        elif obj.status == '3':
            return "未中奖"
        else:
            return "未知"