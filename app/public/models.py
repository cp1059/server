
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