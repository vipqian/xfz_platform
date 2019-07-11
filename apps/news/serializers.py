# -*- coding: utf-8 -*-#

"""
Name:           serializers 
# Author:       wangyunfei
# Date:         2019-06-13
# Description:  
"""

from rest_framework import serializers

from .models import News, Category, Comment
from apps.xfzauth.serializers import AuthorSerializer



class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class NewsSerializer(serializers.ModelSerializer):
    """序列化"""
    category = NewsCategorySerializer()
    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail', 'category', 'author', 'put_time')





class CommentSerizlizer(serializers.ModelSerializer):
    author = AuthorSerializer()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'pub_time', 'count')

    def get_count(self, obj):
        count = Comment.objects.filter(news_id=obj.news_id).count()
        return {'count': count}





