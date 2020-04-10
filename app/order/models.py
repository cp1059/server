
from django.db import models
from lib.utils.mytime import UtilTime

from app.idGenerator import idGenerator

class Order(models.Model):

    """
    订单表
    """

    id = models.BigAutoField(primary_key=True,verbose_name="订单ID")


    orderid = models.CharField(max_length=30,default="")
    userid = models.BigIntegerField(verbose_name="用户代码", null=True)

    amount = models.DecimalField(verbose_name="投注金额",max_digits=18,decimal_places=6,default=0.0)
    num = models.IntegerField(verbose_name="几注",default=0)
    term = models.CharField(verbose_name="期数",max_length=30)

    status = models.CharField(max_length=1,verbose_name="状态,0-待开奖,1-已中奖,2-已撤单,3-未中奖",default="0")
    no = models.CharField(max_length=255,verbose_name="投注号码",default='{"no":[]}')

    gamesid = models.CharField(verbose_name="玩法ID",max_length=20,default='')
    fd = models.DecimalField(verbose_name="投注返点",max_digits=18,decimal_places=6,default=0.0)
    rate = models.CharField(verbose_name="投注赔率",max_length=100,default="")
    cpid = models.IntegerField(verbose_name="彩票ID",default=0)

    createtime = models.BigIntegerField(default=0)
    updtime = models.BigIntegerField(default=0)

    cpurl = None
    cpname = None
    gamename = None
    minitypename = None

    def save(self, *args, **kwargs):

        if not self.orderid:
            self.orderid = idGenerator().ordercode()

        if not self.createtime:
            self.createtime = UtilTime().timestamp
        self.updtime = UtilTime().timestamp
        return super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '订单表'
        verbose_name_plural = verbose_name
        db_table = 'order'