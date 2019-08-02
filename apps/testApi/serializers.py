# -*- coding: utf-8 -*-#

"""
Name:           serializers 
# Author:       wangyunfei
# Date:         2019-07-12
# Description:  
"""

from rest_framework import serializers

from apps.news.models import Banner, Category, Comment, News
from apps.xfzauth.models import User



class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ['content', 'author', 'pub_time']



class NewsDetailSerializers(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'category', 'author', 'put_time', 'comment', 'content', 'count')

    def get_comment(self, obj):
        comment = Comment.objects.filter(news=obj)
        data = CommentSerializer(comment, many=True).data
        return data

    def get_count(self, obj):
        count = Comment.objects.filter(news=obj).count()
        return count





