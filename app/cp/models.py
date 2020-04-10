from django.db import models

from lib.utils.mytime import UtilTime
from app.idGenerator import idGenerator

class Cp(models.Model):

    id=models.AutoField(primary_key=True)

    name = models.CharField(max_length=60,verbose_name="彩票名称",default="")
    sort = models.IntegerField(verbose_name="排序",default=0)

    url = models.CharField(max_length=255,verbose_name="图片地址")

    cptypeid = models.CharField(max_length=20,verbose_name="彩票类型",default="")
    typename = models.CharField(max_length=60,verbose_name="彩票类型名称",default="")

    termnum = models.IntegerField(verbose_name="多少分钟一期",default=0)

    termtot = models.IntegerField(verbose_name="总共多少期,这个可以根据开奖时间和多少分钟一期算出来,算头算尾",default=0,blank=True)

    opentime = models.CharField(max_length=100,default='0030-0310|0730-2350',verbose_name="每天开奖时间")

    type = models.CharField(max_length=1,verbose_name="类型,0-官方,1-私有 官方数据需要做采集",default=0)

    status = models.CharField(max_length=1,verbose_name="状态,0-正常,1-停售,2-维护")

    code = models.TextField(verbose_name="爬虫代码",default='{"code":[]}')
    coderule = models.CharField(max_length=20,verbose_name="期号排序规则",default="")
    cpnorule = models.CharField(max_length=1024,
                                verbose_name="""
                                    {"tot":6,"count":1,"limit":[0,1,2,3,4,5,6,7,8,9]}
                                    开奖号码规则,用在私彩
                                    tot:总共位数,
                                    count:每一位站位多少
                                    limit:号码范围(每一位出奖号码从这里选择)
                                """,
                                default='{}')

    tasktimetable = models.TextField(verbose_name="任务时间表",default='{"tables":[]}',blank=True)

    createtime=models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.createtime:
            self.createtime = UtilTime().timestamp
        return super(Cp, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '彩票'
        verbose_name_plural = verbose_name
        db_table = 'cp'

class CpTermList(models.Model):

    id=models.AutoField(primary_key=True)
    cpid = models.IntegerField(verbose_name="彩票ID")
    cpno = models.CharField(verbose_name="开奖号码",max_length=60,default="")
    currterm = models.CharField(verbose_name="当前期数", max_length=30, default="")
    nextterm = models.CharField(verbose_name="下一期数", max_length=30, default="")
    createtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.createtime:
            self.createtime = UtilTime().timestamp
        return super(CpTermList, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '当前期彩票期数明细'
        verbose_name_plural = verbose_name
        db_table = 'cptermlist'

class CpTermListHistory(models.Model):

    id=models.BigAutoField(primary_key=True)
    cpid = models.IntegerField(verbose_name="彩票ID")
    cpno = models.CharField(verbose_name="开奖号码",max_length=60,default="")
    term = models.CharField(verbose_name="期数", max_length=30, default="")
    createtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.createtime:
            self.createtime = UtilTime().timestamp
        return super(CpTermListHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '彩票期数历史明细'
        verbose_name_plural = verbose_name
        db_table = 'cptermlisthistory'



class CpBigType(models.Model):

    id=models.AutoField(primary_key=True)
    typeid = models.CharField(max_length=20,verbose_name="大类ID",default="")
    name = models.CharField(verbose_name="名称",max_length=60,default="")
    sort = models.IntegerField(default=0,verbose_name="排序")
    createtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):

        if not self.typeid:
            self.typeid = idGenerator().cpbigtype()

        if not self.createtime:
            self.createtime = UtilTime().timestamp
        return super(CpBigType, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '彩票分类大类表'
        verbose_name_plural = verbose_name
        db_table = 'cpbigtype'

class CpSmallType(models.Model):

    id=models.AutoField(primary_key=True)
    bigtypeid = models.CharField(max_length=20,verbose_name="中类ID",default="")
    typeid = models.CharField(max_length=20,verbose_name="中类ID",default="")
    sort = models.IntegerField(default=0,verbose_name="排序")
    name = models.CharField(verbose_name="名称",max_length=60,default="")
    createtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):

        if not self.typeid:
            self.typeid = idGenerator().cpsmalltype()

        if not self.createtime:
            self.createtime = UtilTime().timestamp
        return super(CpSmallType, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '彩票分类中类表'
        verbose_name_plural = verbose_name
        db_table = 'cpsmalltype'

class CpMiniType(models.Model):

    id=models.AutoField(primary_key=True)
    bigtypeid = models.CharField(max_length=20,verbose_name="中类ID",default="")
    smalltypeid = models.CharField(max_length=20,verbose_name="中类ID",default="")
    typeid = models.CharField(max_length=20,verbose_name="小类ID",default="")
    sort = models.IntegerField(default=0,verbose_name="排序")
    name = models.CharField(verbose_name="名称",max_length=60,default="")
    createtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):

        if not self.typeid:
            self.typeid = idGenerator().cpminitype()

        if not self.createtime:
            self.createtime = UtilTime().timestamp
        return super(CpMiniType, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '彩票分类小表'
        verbose_name_plural = verbose_name
        db_table = 'cpminitype'


class CpGames(models.Model):

    id=models.AutoField(primary_key=True)
    bigtypeid = models.CharField(max_length=20,verbose_name="中类ID",default="")
    smalltypeid = models.CharField(max_length=20,verbose_name="中类ID",default="")
    minitypeid = models.CharField(max_length=20,verbose_name="小类ID",default="")
    sort = models.IntegerField(default=0,verbose_name="排序")
    typeid = models.CharField(max_length=20,verbose_name="玩法ID",default="")
    name = models.CharField(verbose_name="名称",max_length=60,default="")

    rules = models.TextField(
            verbose_name="""
                玩法规则
                memo :玩法提示
                    wfts:玩法提示
                    zjsm:中奖说明
                    fl:范例
                ratetype: 赔率方式 0-唯一赔率,1-每一位号码都有赔率,2-指定玩法赔率
                rate: 赔率,当ratetype=='0' 的时候使用此处的值
                rates: 赔率,当ratetype=='2' 的时候使用此处的值
                    此时此处赔率是指定某一玩法的ID 
                    例如：['G0001','G0002']  当满足其中某一条件的时候触发该玩法赔率!
                iscompound: 是否复式 0-是,1-否
                show : 前端显示每一位的号码
                    name: 每一行的名字
                    value: 每一位的具体数据
                        id: 号码
                        rate: 赔率,当ratetype=='1'的时候使用此处的值
                    showhelp: 是否显示帮助信息 0-是,1-否
                    maxminrange: 帮助信息中大小中间值小于等于他，大于他
                    selectrange: 机选范围
                    manyrange: 多选范围
                        
            """,
            default='{"memo":{"wfts":"","zjsm":"","fl":""},"ratetype":"0","rate":"0","iscompound":"1","rates":[],"show":[]}')

    createtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):

        if not self.typeid:
            self.typeid = idGenerator().cpgames()

        if not self.createtime:
            self.createtime = UtilTime().timestamp
        return super(CpGames, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '彩票玩法明细'
        verbose_name_plural = verbose_name
        db_table = 'cpgames'