# -*- coding: utf-8 -*-#

"""
Name:           urls.py
# Author:       wangyunfei
# Date:         2019-05-06
# Description:  
"""

from django.urls import path

from . import  views

app_name = 'payinfo'


urlpatterns = [
    path('index/', views.index, name='index'),
    path('test/', views.test, name='test'),
]
