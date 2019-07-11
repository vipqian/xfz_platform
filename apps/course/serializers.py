# -*- coding: utf-8 -*-#

"""
Name:           serializers 
# Author:       wangyunfei
# Date:         2019-06-13
# Description:  
"""

from rest_framework import serializers
from .models import Course, CourseOrder, Teacher

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('name',)



class CourseListSerializer(serializers.ModelSerializer):

    buy = serializers.SerializerMethodField()
    teacher = TeacherSerializer()
    class Meta:
        model = Course
        fields = ('id', 'title', 'price', 'buy', 'category', 'teacher', 'cover_url')
    def get_buy(self,obj):
        author = self.context['author']
        if author:
            buy = CourseOrder.objects.filter(course=obj, author=author, status=2).exists()
        else:
            buy = False

        return buy