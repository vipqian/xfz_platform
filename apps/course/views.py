from django.shortcuts import render, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.conf import settings


import os, hmac, hashlib, time


from .models import  CourseCategory, Course, CourseOrder
from common import restful
from .forms import BuyCourseForm
from apps.xfzauth.decorators import xfz_login_required

# Create your views here.



def index(request):
    user = request.user
    courses = Course.objects.select_related('teacher', 'category')
    if user.is_authenticated:
        serializer = CourseListSerializer(courses, many=True, context={'author': request.user})
    else:
        serializer = CourseListSerializer(courses, many=True, context={'author': ''})
    data = serializer.data
    return render(request, 'course/course_index.html', context={'courses': data})

def course_detail(request):
    """
    进入到详情页面
    :param request:
    :return:
    """
    form = BuyCourseForm(request.GET)
    if form.is_valid():
        course = form.cleaned_data.get('course_id')
        return render(request, 'course/course_detail.html', context={
            'course': course
        })
    else:
        raise Http404

def course_token(request):
    file = request.GET.get('video')
    course_id = request.GET.get('course_id')
    price = request.GET.get('price')

    if float(price) != 0:
        exists = CourseOrder.objects.filter(author=request.user, course=course_id, status=2).exists()
        if not exists:
            return restful.param_error(message='没有购买')
    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension, '')

    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    return restful.ok(data={'token': token})

@xfz_login_required
def course_order(request):

    form = BuyCourseForm(request.GET)
    if form.is_valid():
        course = form.cleaned_data.get('course_id')
        order = CourseOrder.objects.create(course=course, author=request.user, price=course.price, status=1)
        return render(request, 'course/course_order.html', context={
            'course': course,
            'order': order
        })
    else:
        print(form.get_errors())
        raise Http404




from .serializers import CourseListSerializer
def test(request):
    user = request.user
    courses = Course.objects.all()
    if user.is_authenticated:
        serializer = CourseListSerializer(courses, many=True, context={'author':request.user})
    else:
        serializer = CourseListSerializer(courses, many=True, context={'author':''})
    data = serializer.data
    return restful.ok(data=data)

