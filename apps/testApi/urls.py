# -*- coding: utf-8 -*-#

"""
Name:           urls 
# Author:       wangyunfei
# Date:         2019-07-12
# Description:  
"""

from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/banners/', views.news_banner, name='banners'),
    path('news/category/', views.news_category, name='category'),
    path('news/newsList/', views.news_list, name='category'),
    path('news/newsDetail/', views.news_detail, name='news_detail'),
    path('news/addComment/', views.add_comment, name='add_comment'),
    path('login/', views.login_views, name='login_views'),
]