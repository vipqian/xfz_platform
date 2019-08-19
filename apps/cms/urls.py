"""
@Time    : 2019-04-26
@Author  : 飞
@File    : urls.py
@Software: PyCharm
@brief   : 
"""

from django.urls import path
from . import views, course_views, staff_views

app_name = 'cms'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('write_news/', views.write_news, name='write_news'),
    # 分类列表
    path('category/', views.category_list, name='category'),
    # 新增分类
    path('new_category/', views.new_category, name='new_category'),
    # 进入到新增分类页面
    path('new_category_page/', views.new_category_html, name='new_category_html'),
    # 进入到编辑分类页面
    path('editor_category/', views.editor_category, name='editor_category'),
    # 编辑分类
    path('edit_category/', views.edit_category, name='edit_category'),
    # 删除分类
    path('delete_category/', views.delete_category, name='delete_category'),
    # 上传图片
    path('upload_file/', views.upload_file, name='upload_file'),
    # 获取七牛云token
    path('qntoken/', views.qn_token, name='qntoken'),
    # 添加新闻
    path('add_news/', views.add_news, name='add_news'),
    # 新闻列表
    path('newsList/', views.NewsList.as_view(), name='news_list'),
    # 进入到编辑新闻页面
    path('editor_news_page/', views.editor_news_page, name='editor_news_page'),
    # 删除新闻
    path('delete_news/', views.delete_news, name='delete_news'),
    # 编辑新闻
    path('editor_news/', views.editor_news, name='editor_news'),
    # banner列表
    path('banners/', views.banners, name='banners'),
    # 添加banner
    path('add_banner/', views.add_banner, name='add_banner'),
    # 进入到新增banner页面
    path('write_banner/', views.write_banner, name='write_banner'),
    # 进入到编辑banner页面
    path('editor_banner/', views.editor_banner, name='editor_banner'),
    # 编辑banner
    path('edit_banner/', views.edit_banner, name='edit_banner'),
    # 删除banner
    path('delete_banner/', views.delete_banner, name='delete_banner'),
]

urlpatterns += [
    path('course_list/', course_views.CourseList.as_view(), name='course_list'),
    path('add_course_page/', course_views.add_course_page, name='add_course_page'),
    path('add_course/', course_views.add_course, name='add_course'),
    path('course_category_list/', course_views.course_category_list, name='course_category_list'),
    path('course_add_category_page/', course_views.course_add_category_page, name='course_add_category_page'),
    path('course_add_category/', course_views.course_add_category, name='course_add_category'),
    path('delete_courseCategory/', course_views.delete_courseCategory, name='delete_courseCategory'),
    path('editor_courseCategory_page/', course_views.editor_courseCategory_page, name='editor_courseCategory_page'),
    path('editor_courseCategory/', course_views.editor_courseCategory, name='editor_courseCategory'),
    path('teacher_list/', course_views.teacher_list, name='teacher_list'),
    path('add_teacher_page/', course_views.add_teacher_page, name='add_teacher_page'),
    path('add_teacher/', course_views.add_teacher, name='add_teacher'),
    path('editor_teacher_page/', course_views.editor_teacher_page, name='editor_teacher_page'),
    path('editor_teacher/', course_views.editor_teacher, name='editor_teacher'),
    path('delete_teacher/', course_views.delete_teacher, name='delete_teacher'),
    path('editor_course_page/', course_views.editor_course_page, name='editor_course_page'),
    path('editor_course/', course_views.editor_course, name='editor_course'),
    path('delete_course/', course_views.delete_course, name='delete_course'),

]
urlpatterns += [
    path('staff_list/', staff_views.index, name='staff_list'),
    path('add_staff_page/', staff_views.add_staff_page, name='add_staff_page'),
    path('add_staff/', staff_views.add_staff, name='add_staff'),

]
