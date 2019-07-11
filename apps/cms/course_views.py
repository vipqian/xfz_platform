# -*- coding: utf-8 -*-#

"""
Name:           course_views 
# Author:       wangyunfei
# Date:         2019-06-21
# Description:  课堂页面所有视图
"""

from django.shortcuts import render, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST, require_GET
from django.http import Http404
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.utils.timezone import make_aware
from django.conf import settings
from django.core.paginator import Paginator


from apps.course.models import CourseCategory, Teacher, Course
from .forms import CourseCategoryForm, AddTeacherForm, EditorTeacherForm, AddCourseForm, EditorCourseForm
from common import restful

from datetime import datetime
from urllib import parse

class CourseList(View):
    """新闻列表"""

    def get(self, request):
        """
        新闻列表
        :param request:
        :return:
        """


        page = request.GET.get('p', 1)
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category', '0'))
        teacher_id = int(request.GET.get('teacher', 0))
        courses = Course.objects.select_related('category', 'teacher')

        if start or end:
            if start:
                start_time = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_time = datetime(year=2018, month=1, day=1)

            if end:
                end_time = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_time = datetime.today()
            courses = courses.filter(pub_time__range=(make_aware(start_time), make_aware(end_time)))

        if title:
            courses = courses.filter(title__icontains=title)

        if category_id != 0:
            courses = courses.filter(category=category_id)

        if teacher_id != 0:
            courses = courses.filter(teacher=teacher_id)

        categorys = CourseCategory.objects.all()
        teachers = Teacher.objects.all()
        paginator = Paginator(courses, settings.CMS_ONE_PAGE_NEWS_COUNT)
        try:
            page_obj = paginator.page(page)
            context_data = self.get_pagination_data(paginator, page_obj)



            context = {
                'courses': page_obj.object_list,
                'categorys': categorys,
                'teachers': teachers,
                # 将一个字典变成url
                'context_params': parse.urlencode({
                    'start': start or '',
                    'end': end or '',
                    'title': title or '',
                    'category': category_id or 0,
                    'teacher': teacher_id or 0,
                }),
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category_id': category_id,
                'teacher_id': teacher_id
            }


            context.update(context_data)

            return render(request, 'cms/course/course/course_list.html', context=context)
        except:
            raise Http404


    def get_pagination_data(self, paginator, page_obj, around_count=1):
        """
        :param paginator: paginator对象
        :param page_obj: page_obj对象
        :param around_count: 左右显示的页码的个数
        :return: 分页信息
        """
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        has_next = page_obj.has_next()
        if has_next:
            next_num = page_obj.next_page_number()
        else:
            next_num = 0
        has_previous = page_obj.has_previous()
        if has_previous:
            previous_num = page_obj.previous_page_number()
        else:
            previous_num = 0



        return {
            # 是否有下一页
            'has_next': has_next,
            # 上一页的页码
            'next_num': next_num,
            # 是否有上页
            'has_previous': has_previous,
            # 下一页的页码
            'previous_num': previous_num,
            # 当前页左边的页码
            'left_pages': left_pages,
            # 当前页有点边的页码
            'right_pages': right_pages,
            # 当前页面
            'current_page': current_page,
            # 显示省略
            'left_has_more': left_has_more,
            # 显示省略
            'right_has_more': right_has_more,
            # 总的页数量
            'num_pages': num_pages
        }


@staff_member_required(login_url='news:index')
def add_course_page(request):
    """
    进入到添加课堂列表
    :param request:
    :return:
    """
    categorys = CourseCategory.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'cms/course/course/add_course.html', context={'categorys': categorys, 'teachers': teachers})


@require_POST
def add_course(request):
    """
    添加课程
    :param request:
    :return:
    """
    form = AddCourseForm(request.POST)
    if form.is_valid():
        form.save()
        return restful.ok()
    else:
        print(form.get_errors())
        return restful.param_error(message=form.get_errors())


@staff_member_required(login_url='news:index')
def editor_course_page(request):
    """
    进入到编辑页面
    :param request:
    :return:
    """
    course_id = request.GET.get('course_id')
    try:
        teachers = Teacher.objects.all()
        categorys = CourseCategory.objects.all()
        course = Course.objects.select_related('teacher', 'category').get(pk=course_id)

        return render(request, 'cms/course/course/editor_course.html', context={
            'teachers': teachers,
            'categorys': categorys,
            'course': course
        })
    except ObjectDoesNotExist:
        raise Http404


@require_POST
def editor_course(request):
    """
    对课程进行验证
    :param request:
    :return:
    """

    form = EditorCourseForm(request.POST)
    if form.is_valid():
        course_id = form.cleaned_data.get('course_id')
        title = form.cleaned_data.get('title')
        category = form.cleaned_data.get('category')
        teacher = form.cleaned_data.get('teacher')
        video_url = form.cleaned_data.get('video_url')
        cover_url = form.cleaned_data.get('cover_url')
        price = form.cleaned_data.get('price')
        duration = form.cleaned_data.get('duration')
        profile = form.cleaned_data.get('profile')


        course = Course.objects.get(pk=course_id)
        course.title = title
        course.category = category
        course.teacher = teacher
        course.video_url = video_url
        course.cover_url = cover_url
        course.price = price
        course.duration = duration
        course.profile = profile
        course.save()
        return restful.ok()
    else:
        return restful.param_error(message=form.get_errors())


@staff_member_required(login_url='news:index')
def course_category_list(request):
    """
    进入到课程的分类列表
    :param request:
    :return:
    """
    categorys = CourseCategory.objects.annotate(count=Count('course__id')).order_by('id')
    return render(request, 'cms/course/category/course_category_list.html', context={
        'categorys': categorys
    })


@staff_member_required(login_url='news:index')
def course_add_category_page(request):
    """
    添加课程分类页面
    :param request:
    :return:
    """
    return render(request, 'cms/course/category/add_category.html')

@require_GET
def course_add_category(request):
    """
    添加课程分类
    :param request:
    :return:
    """
    form = CourseCategoryForm(request.GET)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        CourseCategory.objects.create(name=name)
        return redirect(reverse('cms:course_category_list'))
    else:
        errors = form.get_errors()
        return render(request, 'cms/course/category/add_category.html', context={'errors': errors})


@require_GET
def delete_courseCategory(request):
    """
    删除课程分类
    :param request:
    :return:
    """
    category_id = request.GET.get('category_id')
    try:
        CourseCategory.objects.get(id=category_id).delete()
        return render(request, 'cms/course/category/course_category_list.html')
    except ObjectDoesNotExist:
        raise Http404

@staff_member_required(login_url='news:index')
def editor_courseCategory_page(request):
    """
    进入到编辑分类页面
    :param request:
    :return:
    """
    category_id = request.GET.get('category_id')
    try:
        category = CourseCategory.objects.get(pk=category_id)
        return render(request, 'cms/course/category/editor_category.html', context={
            'category': category
        })
    except ObjectDoesNotExist:
        raise Http404


@require_GET
def editor_courseCategory(request):
    """
    编辑分类
    :param request:
    :return:
    """
    category_id = request.GET.get('category_id')
    name = request.GET.get('name')
    try:
        category = CourseCategory.objects.get(pk=category_id)
        category.name = name
        category.save()
        return redirect(reverse('cms:course_category_list'))
    except ObjectDoesNotExist:
        raise Http404

@staff_member_required(login_url='news:index')
def teacher_list(request):
    """
    进入到老师列表页面
    :param request:
    :return:
    """
    teachers = Teacher.objects.all()
    return render(request, 'cms/course/teacher/teacher_list.html', context={
        'teachers': teachers
    })

@require_GET
def delete_teacher(request):
    """
    删除讲师
    :param request:
    :return:
    """
    teacher_id = request.GET.get('teacher_id')
    try:
        Teacher.objects.get(pk=teacher_id).delete()
        return redirect(reverse('cms:teacher_list'))
    except ObjectDoesNotExist:
        raise Http404


@staff_member_required(login_url='news:index')
def add_teacher_page(request):
    """
    进入到添加讲师页面
    :param request:
    :return:
    """
    return render(request, 'cms/course/teacher/add_teacher.html')

@require_POST
def add_teacher(request):
    """
    添加讲师
    :param request:
    :return:
    """
    form = AddTeacherForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        avatar = form.cleaned_data.get('avatar')
        jobtitle = form.cleaned_data.get('jobtitle')
        profile = form.cleaned_data.get('profile')

        Teacher.objects.create(name=name, avatar=avatar, jobtitle=jobtitle, profile=profile)
        return restful.ok()
    else:
        return restful.param_error(message=form.get_errors())


@staff_member_required(login_url='news:index')
def editor_teacher_page(request):
    """
    进入到讲师编辑页面
    :param request:
    :return:
    """
    teacher_id = request.GET.get('teacher_id')
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
        return render(request, 'cms/course/teacher/editor_teacher.html', context={
            'teacher': teacher
        })
    except ObjectDoesNotExist:
        raise Http404


@require_POST
def editor_teacher(request):
    """
    编辑讲师
    :param request:
    :return:
    """
    form = EditorTeacherForm(request.POST)
    if form.is_valid():
        teacher_id = form.cleaned_data.get('teacher_id')
        name = form.cleaned_data.get('name')
        avatar = form.cleaned_data.get('avatar')
        jobtitle = form.cleaned_data.get('jobtitle')
        profile = form.cleaned_data.get('profile')

        Teacher.objects.filter(pk=teacher_id).update(name=name, avatar=avatar, jobtitle=jobtitle, profile=profile)
        return restful.ok()
    else:
        return restful.param_error(message=form.get_errors())


@require_GET
def delete_course(request):
    """
    删除课程
    :param request:
    :return:
    """
    course_id = request.GET.get('course_id')
    try:
        Course.objects.get(pk=course_id).delete()
        return redirect(reverse('cms:course_list'))
    except ObjectDoesNotExist:
        raise Http404



