#-*- coding: utf-8 -*-
"""
@project    : $ {PROJECT_NAME} 
@Time       : 2019-05-05 21:39
@Author     : wangyunfei
@File       : restful.py
@Describe   :
"""

from django.http import JsonResponse



class HttpCode:

    ok = 200
    # 错误的请求
    paramsError = 400
    # 请求错误
    methodError = 405
    # 服务器错误
    serviceError = 500
    # 未授权
    unAuthorError = 401

def ok(code=HttpCode.ok, message='', data=None, **kwargs):
    json_dict = {'code': code, 'message': message, 'data': data}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def param_error(message='', data=None):
    return JsonResponse({'code': HttpCode.paramsError, 'message':message, 'data': data})

def method_error(message='', data=None):
    return JsonResponse({'code': HttpCode.methodError, 'message': message, 'data': data})

def service_error(message='', data=None):
    return JsonResponse({'code': HttpCode.serviceError, 'message': message, 'data': data})

def unAuthor(message='', data=None):
    return JsonResponse({'code': HttpCode.unAuthorError, 'message': message, 'data': data})
