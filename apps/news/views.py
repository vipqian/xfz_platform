from django.shortcuts import render, Http404
from django.conf import settings

from .models import  Category, News, Comment, Banner
from .serializers import NewsSerializer, CommentSerizlizer
from .forms import CommentForms


from common import restful
from apps.xfzauth.decorators import xfz_login_required

# Create your views here.

def index(request):
    categories = Category.objects.all()
    banners = Banner.objects.all()
    if banners.count() > 5:
        banners = banners[:5]
    # newses = News.objects.all()[:settings.ONE_PAGE_NEWS_COUNT]
    newses = News.objects.select_related('category').all()[:settings.ONE_PAGE_NEWS_COUNT]
    return render(request, 'news/index.html', context={
        'categories': categories,
        'newses': newses,
        'banners': banners
    })


def list_news(request):
    """
    获取新闻列表
    :param request:
    :return:
    """
    page = int(request.GET.get('page', 1))
    category_id = int(request.GET.get('category_id', 0))
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT
    if category_id == 0:
        newses = News.objects.select_related('category').all()[start:end]
    else:
        newses = News.objects.select_related('category').filter(category=category_id)[start:end]
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    return restful.ok(data=data)

def new_detail(request, news_id):
    """
    进入到新闻详情页面
    :param request:
    :param news_id: 新闻的id
    :return:
    """
    try:
        news = News.objects.select_related('category').get(pk=news_id)
        count = Comment.objects.filter(news_id=news_id).count()
        comments = Comment.objects.select_related('author').filter(news_id=news_id)
        return render(request, 'news/news_detail.html', context={'news': news, 'comments': comments, 'count': count})
    except:
        raise Http404


@xfz_login_required
def comment_list(request):
    """
    发表评论
    :param request:
    :param news_id:
    :return:
    """
    forms = CommentForms(request.GET)
    if forms.is_valid():
        content = forms.cleaned_data.get('content')
        news_id = forms.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content, news=news, author=request.user)
        serizlize = CommentSerizlizer(comment)
        return restful.ok(data=serizlize.data)
    else:
        return restful.param_error(data=forms.get_errors())






def search(request):
    return render(request, 'search/search1.html')


