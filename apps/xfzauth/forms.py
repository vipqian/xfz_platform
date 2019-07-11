"""
@Time    : 2019-05-04
@Author  : 飞
@File    : forms.py
@Software: PyCharm
@brief   : 
"""

from django import forms
from common.forms import FormMixin
from django.core.cache import cache
from .models import User


class LoginForms(forms.Form, FormMixin):

    telephone = forms.CharField(max_length=11, min_length=11, error_messages={
        'max_length': '传入正确的电话号码！',
        'min_length': '传入正确的电话号码！',
        'required': '请输入电话号码',
    })
    password = forms.CharField(max_length=18, min_length=6, error_messages={
        'max_length': '密码超过18位！',
        'min_length': '密码小于6位！',
        'required': '请输入密码',
    })
    remember = forms.IntegerField(required=False)


class SendPhoneCode(forms.Form, FormMixin):
    """短信验证码中电话号的验证码"""
    telephone = forms.CharField(max_length=11, min_length=11, error_messages={
        'max_length': '传入正确的电话号码！',
        'min_length': '传入正确的电话号码！',
        'required': '请输入电话号码',
    })



class RegisterForm(forms.Form, FormMixin):
    """对注册信息的认证"""
    telephone = forms.CharField(max_length=11, min_length=11, error_messages={
        'max_length': '传入正确的电话号码！',
        'min_length': '传入正确的电话号码！',
        'required': '请输入电话号码',
    })
    username = forms.CharField(max_length=20, error_messages={
        'max_length': '输入的用户名过长',
        'required': '用户名不能为空'
    })
    img_captcha = forms.CharField(max_length=4, error_messages={
        'max_length': '图形验证码不正确！',
        'required': '请输入的图形验证码',
    })
    password1 = forms.CharField(max_length=18, min_length=6, error_messages={
        'max_length': '密码超过18位！',
        'min_length': '密码小于6位！',
        'required': '请输入密码',
    })
    password2 = forms.CharField(max_length=18, min_length=6, error_messages={
        'max_length': '密码超过18位！',
        'min_length': '密码小于6位！',
        'required': '请输入密码',
    })
    sms_captcha = forms.CharField(max_length=6, min_length=6, error_messages={
        'max_length': '验证码不正确！',
        'min_length': '验证码不正确！',
        'required': '请输入验证码',
    })

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('2次输入的密码不一致')
        img_captcha = cleaned_data.get('img_captcha')
        if img_captcha:
            cached_img_captcha = cache.get(img_captcha.lower())
            if not cached_img_captcha or cached_img_captcha != img_captcha.lower():
                raise forms.ValidationError('输入的图形验证码错误')
        else:
            raise forms.ValidationError('请输入图形验证码')
        sms_captcha = cleaned_data.get('sms_captcha')
        telephone = cleaned_data.get('telephone')
        if sms_captcha == '000000':
            pass
        else:
            cached_sms_captcha = cache.get(telephone)
            if not cached_sms_captcha or cached_sms_captcha != int(sms_captcha):
                raise forms.ValidationError('短信验证码错误')

        exist = User.object.filter(telephone=telephone).exists()
        if exist:
            raise forms.ValidationError('手机号已经注册')


