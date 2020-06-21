
from django.db import models
from lib.utils.mytime import UtilTime

class Banner(models.Model):

    id=models.AutoField(primary_key=True)
    url = models.CharField(max_length=255,verbose_name="地址")
    type = models.CharField(max_length=1,verbose_name="0-图片,1-视频")
    link = models.CharField(max_length=255,verbose_name="链接的页面",default="",blank=True)
    sort = models.IntegerField(default=0)
    createtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.createtime:
            self.createtime = UtilTime().timestamp
        return super(Banner, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        db_table = 'banner'

class Holiday(models.Model):

    id=models.AutoField(primary_key=True)
    year = models.CharField(max_length=4,verbose_name="年")

    start_date = models.CharField(max_length=5,verbose_name="开始日期")
    end_date = models.CharField(max_length=5,verbose_name="日期")
    memo = models.CharField(max_length=60,verbose_name="说明")

    class Meta:
        verbose_name = '节假日表(停止售彩)'
        verbose_name_plural = verbose_name
        db_table = 'holiday'


class Video(models.Model):

    id=models.AutoField(primary_key=True)
    url = models.CharField(max_length=255,verbose_name="地址")
    sort = models.IntegerField(default=0)
    createtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.createtime:
            self.createtime = UtilTime().timestamp
        return super(Video, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '视频表'
        verbose_name_plural = verbose_name
        db_table = 'video'