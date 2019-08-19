# -*- coding: utf-8 -*-#

"""
Name:           staff_views 
# Author:       wangyunfei
# Date:         2019-08-12
# Description:  
"""
from django.shortcuts import render, redirect, reverse
from apps.xfzauth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages


def index(request):
    users = User.object.filter(is_staff=True)
    return render(request, 'cms/staffs/staffs_list.html', context={'staffs': users})

def add_staff_page(request):
    groups = Group.objects.all()
    return render(request, 'cms/staffs/add_user.html', context={'groups': groups})

def add_staff(request):
    telephone = request.POST.get('telephone')
    user = User.object.filter(telephone=telephone).first()
    print(user.username)
    if user:
        user.is_staff = True
        group_ids = request.POST.getlist("groups")
        groups = Group.objects.filter(pk__in=group_ids)
        print(groups)
        user.groups.set(groups)
        user.save()
        return redirect(reverse('cms:staff_list'))
    else:
        messages.info(request, '手机号码不存在！')
        return redirect(reverse('cms:add_staff'))
