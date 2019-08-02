from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, login

# Create your views here.


from common import restful

from apps.news.models import Banner, Category, News, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


from .serializers import BannerSerializers, CategorySerializers, NewsDetailSerializers
from apps.news.serializers import NewsSerializer


from .forms import NewsDetailForms, AddCommentForms, LoginForms





def index(request):
    return restful.ok()



def news_banner(request):
    """
    获取banner接口
    :param request:
    :return:
    """
    banners = Banner.objects.all()
    serializers = BannerSerializers(banners, many=True)
    print(serializers.data)
    return restful.ok(data=serializers.data)

def news_category(request):
    """
    获取分类接口
    :param request:
    :return:
    """
    categorys = Category.objects.all()
    serializers = CategorySerializers(categorys, many=True)
    return restful.ok(data=serializers.data)


def news_list(request):
    """
    获取新闻列表接口
    :param request:
    :return:
    """

    page = int(request.GET.get('page', 1))
    category_id = int(request.GET.get('category_id', 0))
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT
    if category_id == 0:
        newses = News.objects.select_related('category').all()[start:end]
    else:
        newses = News.objects.select_related('category').filter(category=category_id)[start:end]
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    return restful.ok(data=data)


def news_detail(request):
    """
    新闻详情接口
    :param request:
    :return:
    """
    forms = NewsDetailForms(request.GET)
    if forms.is_valid():
        news_id = forms.cleaned_data.get('news_id')
        print(news_id)
        news = News.objects.get(pk=news_id)
        serializer = NewsDetailSerializers(news)
        return restful.ok(data=serializer.data)
    else:
        return restful.param_error(message=forms.get_errors())


def add_comment(request):
    """
    添加评论
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        forms = AddCommentForms(request.GET)
        if forms.is_valid():
            content = forms.cleaned_data.get('content')
            news_id = forms.cleaned_data.get('news_id')
            Comment.objects.create(news_id=news_id, content=content, author=request.user)
            return restful.ok(message='发表成功')
        else:
            return restful.param_error(message=forms.get_errors())

    else:
        return restful.param_error(message='请登录')


def login_views(request):
    """
    登录接口
    :param request:
    :return:
    """
    form = LoginForms(request.GET)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, telephone=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok(message='登录成功')
            else:
                return restful.unAuthor(message='账号已经被冻结')
        else:
            return restful.param_error(message='账号或密码错误')
    else:
        return restful.param_error(message=form.get_errors())


