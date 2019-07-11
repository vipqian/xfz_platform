from django.shortcuts import render, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.http import Http404
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.core.paginator import Paginator
from django.utils.timezone import make_aware


import os
import qiniu
from datetime import datetime
# 将字典变成url形式
from urllib import parse



from .forms import CategoryForms, AddNewsForm, AddBannerForm, EditorBannerForm, EditorNewsForm
from apps.news.models import Category, News, Banner
from common import restful

# Create your views here.
@staff_member_required(login_url="news:index")
def index(request):
    return render(request, 'cms/news/index.html')


@staff_member_required(login_url='news:index')
def write_news(request):
    """
    进入到添加新闻页面
    :param request:
    :return:
    """
    categorys = Category.objects.all()

    return render(request, 'cms/news/write_news.html', context={'categorys': categorys})


@staff_member_required(login_url='news:index')
@require_POST
def add_news(request):
    """
    添加新闻
    :param request:
    :return:
    """
    form = AddNewsForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        desc = form.cleaned_data.get('desc')
        thumbnail = form.cleaned_data.get('thumbnail')
        category_id = form.cleaned_data.get('category')
        content = form.cleaned_data.get('content')
        category = Category.objects.get(pk=category_id)
        author = form.cleaned_data.get('author')
        if author:
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail,
                                category=category, author=author, content=content)
        else:
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail,
                                category=category, author=request.user.username,
                                content=content)
        return restful.ok()

    else:
        return restful.param_error(message=form.get_errors())


@staff_member_required(login_url='news:index')
def category_list(request):
    """
    新闻分类
    :param request:
    :return:
    """
    categorys = Category.objects.annotate(count=Count('news__id')).order_by('id')
    return render(request, 'cms/news/category_list.html', context={'categorys': categorys})


@staff_member_required(login_url='news:index')
def new_category_html(request):
    """
    进入到新增分类页面
    :param request:
    :return:
    """
    return render(request, 'cms/news/new_category.html')


@staff_member_required(login_url='news:index')
def new_category(request):
    """
    添加分类
    :param request:
    :return:
    """
    forms = CategoryForms(request.GET)
    if forms.is_valid():
        name = forms.cleaned_data.get('name')
        Category.objects.create(name=name)
        return redirect(reverse('cms:category'))
    else:
        errors = forms.get_errors()
        return render(request, 'cms/news/new_category.html', context={'errors': errors})


@staff_member_required(login_url='news:index')
def delete_category(request):
    """
    删除分类
    :param request:
    :return:
    """
    category_id = request.GET.get('category_id')
    Category.objects.get(id=category_id).delete()
    return redirect(reverse('cms:category'))


@staff_member_required(login_url='news:index')
def editor_category(request):
    """
    跳转到分类编辑页面
    :param request:
    :return:
    """
    category_id = request.GET.get('category_id')
    try:

        category = Category.objects.get(pk=category_id)
        return render(request, 'cms/news/editor_category.html', context={'category': category})
    except ObjectDoesNotExist:
        raise Http404


@staff_member_required(login_url='news:index')
def edit_category(request):
    """
    编辑分类
    :param request:
    :return:
    """
    category_id = request.GET.get('category_id')
    name = request.GET.get('name')
    try:

        category = Category.objects.get(pk=category_id)
        category.name = name
        category.save()
        return redirect(reverse('cms:category'))
    except ObjectDoesNotExist:
        raise Http404


@require_POST
@staff_member_required(login_url='news:index')
def upload_file(request):
    """
    上传文件
    :param request:
    :return:
    """
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    # request.build_absolute_uri()作用是拼接路径，http://127.0.0.1:8000
    url = request.build_absolute_uri(settings.MEDIA_URL+name)

    return restful.ok(data={'url': url})


@require_GET
def qn_token(request):
    """
    获取七牛云token
    :param request:
    :return:
    """
    access_key = 'd9W4xj9mndRr3ovMFBuzvHGhc13XjVdi2GzT8XsU'
    secret_key = 'eRf9a2qSfHd_4R8QHCh32AJr4szxu-pGC84KtH77'

    bucket = 'xfz_platfrom'
    q = qiniu.Auth(access_key, secret_key)

    token = q.upload_token(bucket)
    return restful.ok(data={'token': token})


@staff_member_required(login_url='news:index')
def news_list(request):
    """
    新闻列表
    :param request:
    :return:
    """
    newses = News.objects.select_related('category').all().values('id', 'title', 'desc', 'thumbnail', 'put_time', 'author', 'category__name')
    categorys = Category.objects.all()
    return render(request, 'cms/news/news_list.html', context={'newses': newses,
                                                          'categorys': categorys})



class NewsList(View):
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

        newses = News.objects.select_related('category')
        if start or end:
            if start:
                start_time = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_time = datetime(year=2018, month=1, day=1)

            if end:
                end_time = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_time = datetime.today()
            newses = newses.filter(put_time__range=(make_aware(start_time), make_aware(end_time)))

        if title:
            newses = newses.filter(title__icontains=title)

        if category_id != 0:
            newses = newses.filter(category=category_id)

        categorys = Category.objects.all()
        paginator = Paginator(newses, settings.CMS_ONE_PAGE_NEWS_COUNT)
        try:
            page_obj = paginator.page(page)
            context_data = self.get_pagination_data(paginator, page_obj)



            context = {
                'newses': page_obj.object_list,
                'categorys': categorys,
                # 将一个字典变成url
                'context_params': parse.urlencode({
                    'start': start or '',
                    'end': end or '',
                    'title': title or '',
                    'category': category_id or 0
                }),
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category_id': category_id
            }


            context.update(context_data)

            return render(request, 'cms/news/news_list.html', context=context)
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
def banners(request):
    """
    banner列表
    :param request:
    :return:
    """
    banner_list = Banner.objects.all().order_by('-pub_time')
    return render(request, 'cms/news/banner.html', context={'banners': banner_list})


@staff_member_required(login_url='news:index')
def add_banner(request):
    """
    添加banner页面
    :param request:
    :return:
    """
    return render(request, 'cms/news/add_banner.html')


@require_POST
def write_banner(request):
    """
    添加banner接口
    :param request:
    :return:
    """
    form = AddBannerForm(request.POST)
    if form.is_valid():
        image_url = form.cleaned_data.get('image_url')
        priority = form.cleaned_data.get('priority')
        link_to = form.cleaned_data.get('link_to')
        Banner.objects.create(image_url=image_url, priority=priority, link_to=link_to)

        return restful.ok(message='添加成功')
    else:
        return restful.param_error(message=form.get_errors())


@staff_member_required(login_url='news:index')
def editor_banner(request):
    """
    进入到编辑页面
    :param request:
    :return:
    """
    banner_id = request.GET.get('banner_id')
    try:
        banner = Banner.objects.get(id=banner_id)
        return render(request, 'cms/news/editor_banner.html', context={'banner': banner})
    except ObjectDoesNotExist:
        raise Http404


@staff_member_required(login_url='news:index')
@require_POST
def edit_banner(request):
    """
    编辑banner
    :param request:
    :return:
    """
    form = EditorBannerForm(request.POST)
    if form.is_valid():
        banner_id = form.cleaned_data.get('banner_id')
        image_url = form.cleaned_data.get('image_url')
        priority = form.cleaned_data.get('priority')
        link_to = form.cleaned_data.get('link_to')

        try:
            banner = Banner.objects.get(id=banner_id)
            banner.image_url = image_url
            banner.priority = priority
            banner.link_to = link_to
            banner.save()
            return restful.ok()
        except ObjectDoesNotExist:
            raise Http404
    else:
        return restful.param_error(message=form.get_errors())


@staff_member_required(login_url='news:index')
@require_GET
def delete_banner(request):
    """
    删除banner
    :param request:
    :return:
    """
    banner_id = request.GET.get('banner_id')
    try:
        banner = Banner.objects.get(pk=banner_id)
        banner.delete()
        return redirect(reverse('cms:banners'))
    except ObjectDoesNotExist:
        raise Http404


@require_GET
@staff_member_required(login_url='news:index')
def delete_news(request):
    """
    删除新闻
    :param request:
    :return:
    """
    news_id = request.GET.get('news_id')
    try:
        news = News.objects.get(pk=news_id)
        news.delete()
        return redirect(reverse('cms:news_list'))
    except ObjectDoesNotExist:
        raise Http404


@staff_member_required(login_url='news:index')
def editor_news_page(request):
    """
    进入到编辑新闻页面
    :param request:
    :return:
    """
    news_id = request.GET.get('news_id')
    categorys = Category.objects.all()
    try:
        news = News.objects.get(pk=news_id)
        return render(request, 'cms/news/editor_news.html', context={'news': news, 'categorys': categorys})
    except ObjectDoesNotExist:
        raise Http404


@staff_member_required(login_url='news:index')
@require_POST
def editor_news(request):
    """
    编辑新闻
    :param request:
    :return:
    """
    form = EditorNewsForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        title = form.cleaned_data.get('title')
        desc = form.cleaned_data.get('desc')
        thumbnail = form.cleaned_data.get('thumbnail')
        category_id = form.cleaned_data.get('category')
        content = form.cleaned_data.get('content')
        category = Category.objects.get(pk=category_id)
        author = form.cleaned_data.get('author')

        try:
            news = News.objects.get(pk=news_id)
            news.title = title
            news.desc = desc
            news.thumbnail = thumbnail
            news.category = category
            news.content = content
            news.author = author
            news.save()
            return restful.ok()
        except ObjectDoesNotExist:
            raise Http404
    else:
        return restful.param_error(message=form.get_errors())
