# -*- coding: utf-8 -*-#

"""
Name:           staff_views 
# Author:       wangyunfei
# Date:         2019-08-12
# Description:  
"""
from django.shortcuts import render
from apps.xfzauth.models import User


def index(request):
    users = User.object.filter(is_staff=True)
    return render(request, 'cms/staffs/staffs_list.html', context={'staffs': users})
