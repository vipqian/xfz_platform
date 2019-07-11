from django.db import models

from shortuuidfield import ShortUUIDField

# Create your models here.

class PayInfo(models.Model):

    title = models.CharField(max_length=100)
    profile = models.CharField(max_length=200)
    price = models.FloatField()
    # 文件存储路径
    path = models.FilePathField()
    pub_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-pub_time']


class PayinfoOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    payinfo = models.ForeignKey('PayInfo', on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey('xfzauth.User', on_delete=models.DO_NOTHING)
    price = models.IntegerField(default=0)
    # 付款方式， 1代表微信，2代表支付宝
    istype = models.SmallIntegerField(default=0)
    # 代表是否支付，1代表未支付，2代表支付成功
    status = models.SmallIntegerField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_time']

