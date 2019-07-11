# -*- coding: utf-8 -*-#

"""
Name:           decorators 
# Author:       wangyunfei
# Date:         2019-06-18
# Description:  装饰器
"""
from common import restful


from django.shortcuts import redirect, reverse


def xfz_login_required(fun):

    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:
            return fun(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unAuthor(message='请登录')
            else:
                return redirect(reverse('news:index'))
    return wrapper
