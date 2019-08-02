# -*- coding: utf-8 -*-#

"""
Name:           forms
# Author:       wangyunfei
# Date:         2019-07-12
# Description:  
"""

from django import forms
from apps.news.models import News

from common.forms import FormMixin


class NewsDetailForms(forms.Form, FormMixin):

    news_id = forms.IntegerField()


    def clean(self):
        cleaned_data = super(NewsDetailForms, self).clean()
        news_id = cleaned_data.get('news_id')
        exists = News.objects.filter(pk=news_id).exists()
        if not exists:
            raise forms.ValidationError('文章不存在')

class AddCommentForms(forms.Form, FormMixin):
    news_id = forms.IntegerField(error_messages={
        'required': '没有传入文章ID',
    })
    content = forms.CharField(max_length=200, error_messages={
        'max_length': '输入超过200字符！',
        'required': '请输入评论',
    })

    def clean(self):
        cleaned_data = super(AddCommentForms, self).clean()
        news_id = cleaned_data.get('news_id')
        print(news_id)
        if news_id != None:
            exists = News.objects.filter(pk=news_id).exists()
            if not exists:
                raise forms.ValidationError('文章ID不正确')


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


