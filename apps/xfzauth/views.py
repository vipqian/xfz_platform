from django.shortcuts import render, redirect, reverse
# 限制请求
from django.views.decorators.http import require_POST
# 登录
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
# 缓存
from django.core.cache import cache
# 获取User
from django.contrib.auth import get_user_model

User = get_user_model()


from .forms import LoginForms, SendPhoneCode, RegisterForm
from common import restful
from common import send_telephone_code as send
from common.captcha.xfz_captcha import Captcha

from io import BytesIO
import random

# Create your views here.


@require_POST
def login_views(request):
    """
    登录
    :param request:
    :return:
    """
    form = LoginForms(request.POST)

    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    # 设置浏览器的session的过期时间为django默认的时间（2个星期）
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unAuthor(message='您的账号已经被冻结！')
        else:
            return restful.param_error(message='手机号或密码错误')
    else:
        errors = form.get_errors()
        return restful.param_error(message=errors)



def logout_views(request):
    """
    退出
    :param request:
    :return:
    """
    logout(request)
    return redirect(reverse("news:index"))



def img_captcha(request):
    """
    获取验证码图片
    :param request:
    :return:
    """
    text, image = Captcha.gene_code()
    # 存在在缓存中
    cache.set(text.lower(), text.lower(), 5*60)
    # BytesIO相当一个管道，存储图片的数据流
    print(text)
    out = BytesIO()
    # 将image的图片存储到管道中
    image.save(out, 'png')
    # 将BytesIo的指针移动到文件最开始的地方
    out.seek(0)


    response = HttpResponse(content_type='image/png')
    # 将BytesIo中的图片移动到response中
    response.write(out.read())
    # 告诉图片的大小
    response['Content-length'] = out.tell()

    return response


def sms_captcha(request):
    """
    发送短信验证码
    :param request:
    :return:
    """
    form = SendPhoneCode(request.GET)
    if form.is_valid():
        telephone = request.GET.get('telephone')
        code = random.randint(100000, 999999)
        cache.set(telephone, code, 5*60)
        # cache.set('17600661017', '000000', 5*60)
        result = send.sms_captcha_sender(telephone, code)
        if result:
            return restful.ok()
        else:
            return restful.param_error(message='短信验证码发送失败')
    else:
        errors = form.get_errors()
        return restful.param_error(message=errors)

@require_POST
def register(request):
    """
    注册
    :param request:
    :return:
    """
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.object.create_user(telephone=telephone, username=username, password=password)
        login(request, user)
        return restful.ok()
    else:
        error = form.get_errors()
        return restful.param_error(message=error)





