# -*- coding: utf-8 -*-#

"""
Name:           initgroup
# Author:       wangyunfei
# Date:         2019-08-12
# Description:  
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, ContentType


from apps.news.models import News, Category, Banner, Comment
from apps.course.models import Course, CourseCategory, Teacher, CourseOrder
from apps.payinfo.models import PayInfo, PayinfoOrder

class Command(BaseCommand):
    """编辑分组"""
    def handle(self, *args, **options):
        # 1.创建分组(管理新闻的权限）
        content_type = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(Category),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Teacher),
            ContentType.objects.get_for_model(PayInfo),
        ]
        edit_permission = Permission.objects.filter(content_type__in=content_type)
        edit_group = Group.objects.create(name='编辑')
        edit_group.permissions.set(edit_permission)
        edit_group.save()
        self.stdout.write(self.style.SUCCESS('编辑创建成功'))

        # 2创建财务组
        finance_content_type = [
            ContentType.objects.get_for_model(PayinfoOrder),
            ContentType.objects.get_for_model(CourseOrder),
        ]
        finance_permission = Permission.objects.filter(content_type__in=finance_content_type)
        finance_group  = Group.objects.create(name='财物')
        finance_group.permissions.set(finance_permission)
        self.stdout.write(self.style.SUCCESS('财物创建成功'))

        # 3.创建管理员组
        # 就是把第一和第二的权限链接在一起 queryset对象可以通过union链接在一起
        admin_permission = edit_permission.union(finance_permission)
        admin_group = Group.objects.create(name='管理员')
        admin_group.permissions.set(admin_permission)
        admin_group.save()
        self.stdout.write(self.style.SUCCESS('管理员创建成功'))

        # 4.创建超级管理员组
