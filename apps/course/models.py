from django.db import models

# Create your models here.


class CourseCategory(models.Model):
    name = models.CharField(max_length=20)


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    # 头像
    avatar = models.URLField()
    # 职务
    jobtitle = models.CharField(max_length=100)
    # 简介
    profile = models.TextField()



class Course(models.Model):

    title = models.CharField(max_length=200)
    category = models.ForeignKey('CourseCategory', on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey('Teacher', on_delete=models.DO_NOTHING)
    video_url = models.URLField()
    # 封面图
    cover_url = models.URLField()
    price = models.FloatField(default=0)
    # 时长
    duration = models.IntegerField()
    # 简介
    profile = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_time']



class CourseOrder(models.Model):

    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING)
    author = models.ForeignKey('xfzauth.User', on_delete=models.DO_NOTHING)

    price = models.IntegerField(default=0)
    # 付款方式， 1代表微信，2代表支付宝
    istype = models.SmallIntegerField(default=0)
    #代表是否支付，1代表未支付，2代表支付成功
    status = models.SmallIntegerField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-pub_time']

