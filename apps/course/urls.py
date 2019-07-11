#-*- coding: utf-8 -*-
"""
@project    : $ {PROJECT_NAME} 
@Time       : 2019-05-06 15:32
@Author     : wangyunfei
@File       : urls.py
@Describe   :
"""

from django.urls import path

from . import views


app_name = 'course'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detail/', views.course_detail, name='course_detail'),
    path('course_token/', views.course_token, name='course_token'),
    path('course_order/', views.course_order, name='course_order'),
    path('test/', views.test, name='test'),



]
