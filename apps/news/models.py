from django.db import models

# Create your models here.


class Category(models.Model):
    """新闻分类"""
    name = models.CharField(max_length=100)
    # PositiveIntegerField该类型的值只允许为正整数或 0
    # count = models.PositiveIntegerField(default=0)
    #
    #
    # # 添加新闻自动加一
    # def increase_news(self):
    #     self.count += 1
    #     self.save(update_fields=['count'])


class News(models.Model):
    """新闻"""
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    # 创建时间
    put_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.CharField(max_length=100, null=True)


    class Meta:
        ordering = ['-put_time']


class Comment(models.Model):
    """评论"""
    content = models.CharField(max_length=200)
    author = models.ForeignKey('xfzauth.User', on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-pub_time']




class Banner(models.Model):
    priority = models.IntegerField(default=0)
    image_url = models.URLField()
    link_to = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['priority', '-pub_time']