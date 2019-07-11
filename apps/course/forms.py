# -*- coding: utf-8 -*-#

"""
Name:           forms 
# Author:       wangyunfei
# Date:         2019-06-25
# Description:  
"""


from django import forms



from .models import Course
from common.forms import FormMixin


class BuyCourseForm(FormMixin, forms.Form):
    course_id = forms.IntegerField()

    def clean_course_id(self):
        course_id = self.cleaned_data.get('course_id')
        course = Course.objects.filter(pk=course_id)
        exists = course.exists()
        if not exists:
            raise forms.ValidationError('课程不存在或')
        return course.first()

