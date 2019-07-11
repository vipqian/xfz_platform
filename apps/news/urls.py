"""
@Time    : 2019-05-04
@Author  : 飞
@File    : urls.py
@Software: PyCharm
@brief   : 
"""


from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('index/',  views.index, name='index'),
    # path('<int:news_id>/',  views.new_detail, name='news_detail'),
    path('detail/<int:news_id>/', views.new_detail, name='news_detail'),

    path('search/',  views.search, name='search'),
    # 获取每一页的新闻
    path('list/', views.list_news, name='list_news'),
    # 评论
    path('comment_list/', views.comment_list, name='comment_list'),

]
