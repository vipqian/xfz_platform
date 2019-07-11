"""
@Time    : 2019-05-05
@Author  : 飞
@File    : urls.py
@Software: PyCharm
@brief   : 
"""

from django.urls import path
from . import views

app_name = 'xfzauth'

urlpatterns = [
    path('login/', views.login_views, name='login'),
    path('logout/', views.logout_views, name='logout'),
    path('image/', views.img_captcha, name='image'),
    path('sms_captcha/', views.sms_captcha, name='sms_captcha'),
    path('register/', views.register, name='register'),


]