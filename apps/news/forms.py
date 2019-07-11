# -*- coding: utf-8 -*-#

"""
Name:           forms.py
# Author:       wangyunfei
# Date:         2019-06-17
# Description:  
"""

from django import forms


from common.forms import FormMixin


class CommentForms(forms.Form, FormMixin):
    """对评论提交的表单进行验证码"""
    content = forms.CharField(max_length=200, error_messages={
        'max_length': '输入超过200字符！',
        'required': '请输入评论',
    })
    news_id = forms.IntegerField()

