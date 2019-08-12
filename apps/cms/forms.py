# -*- coding: utf-8 -*-#

"""
Name:           forms 
# Author:       wangyunfei
# Date:         2019-05-12
# Description:  
"""

from django import forms

from common.forms import FormMixin
from apps.news.models import Category, News, Banner
from apps.course.models import CourseCategory, Teacher, Course

class CategoryForms(forms.Form, FormMixin):
    """表单验证"""
    name = forms.CharField(max_length=100, min_length=1, error_messages={
        "max_length": '请填写长度为1到100的分类名字',
        "min_length": '请填写长度为1到100的分类名字',
        "required": '请填写分类名称'
    })

    def clean(self):
        cleaned_data = super(CategoryForms, self).clean()
        name = cleaned_data.get('name')
        exists = Category.objects.filter(name=name).exists()
        if exists:
            raise forms.ValidationError('分类已经存在')


class AddNewsForm(forms.ModelForm, FormMixin):
    """添加新闻表单验证"""
    category = forms.IntegerField()
    class Meta:
        model = News
        exclude = ['put_time', 'category']
        error_messages = {
            'title': {
                'max_length': '长度不能超过20个字符',
                'required': '标题不能为空'
            },
            'desc': {
                'max_length': '长度不能超过20个字符',
                'required': '描述不能为空'
            },
            'content': {
                'required': '内容不能为空'
            },
            'thumbnail': {
                'required': '请上传图片'
            }
        }


class AddBannerForm(forms.ModelForm, FormMixin):
    """添加banner表单验证"""
    class Meta:
        model = Banner
        fields = "__all__"



class EditorBannerForm(forms.Form, FormMixin):
    """对编辑banner表单验证"""
    banner_id = forms.IntegerField()
    image_url = forms.URLField()
    priority = forms.IntegerField()
    link_to = forms.URLField()


class EditorNewsForm(AddNewsForm):
    """编辑新闻表单"""
    news_id = forms.IntegerField()

    def clean_news_id(self):
        news_id = self.cleaned_data.get('news_id')
        exists = News.objects.filter(pk=news_id).exists()
        if not exists:
            raise forms.ValidationError('文章已存在')
        return news_id



class CourseCategoryForm(forms.ModelForm, FormMixin):
    class Meta:
        model = CourseCategory
        fields = "__all__"


class AddTeacherForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Teacher
        fields = "__all__"

        error_messages = {
            'name': {
                'max_length': '长度不能超过100个字符',
                'required': '姓名不能为空'
            },
            'avatar': {
                'required': '头像不能为空'
            },
            'jobtitle': {
                'max_length': '长度不能超过100个字符',
                'required': '职务不能为空'
            },
            'profile': {
                'required': '简介不能为空'
            },
        }



class EditorTeacherForm(AddTeacherForm):
    teacher_id = forms.IntegerField()

    def clean_teacher_id(self):
        teacher_id = self.cleaned_data.get('teacher_id')
        exists = Teacher.objects.filter(pk=teacher_id).exists()
        if not exists:
            raise forms.ValidationError(message='讲师已经存在')
        return teacher_id


class AddCourseForm(FormMixin, forms.ModelForm):

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('价格不能小于0')

    class Meta:
        model = Course
        exclude = ['price']


        error_messages = {
            'title': {
                'max_length': '长度不能超过200个字符',
                'required': '标题不能为空'
            },
            'video_url': {
                'required': '视频地址不能为空'
            },
            'cover_url': {
                'required': '封面不能为空'
            },
            'duration': {
                'required': '时长不能为空'
            },
            'price': {
                'required': '价格不能为空'
            },

            'profile': {
                'required': '简介不能为空'
            },
        }


class EditorCourseForm(AddCourseForm):
    course_id = forms.IntegerField()

    def clean_course(self):
        course_id = self.cleaned_data.get('course_id')
        exists = Course.objects.filter(pk=course_id).exists()
        if not exists:
            raise forms.ValidationError('课程不存在')
        return course_id


