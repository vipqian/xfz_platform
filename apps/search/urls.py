# -*- coding: utf-8 -*-#

"""
Name:           urls 
# Author:       wangyunfei
# Date:         2019-06-28
# Description:  
"""

from django.urls import path
from . import views


app_name = 'search'


urlpatterns = [
    path('', views.index, name='index')
]