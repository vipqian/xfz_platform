"""xfz_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from apps.news import views



urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('news/', include(('apps.news.urls', 'apps.news'), namespace='news')),
    path('cms/', include(('apps.cms.urls', 'apps.cms'), namespace='cms')),
    path('account/', include(('apps.xfzauth.urls', 'apps.xfzauth'), namespace='xfzauth')),
    path('course/', include(('apps.course.urls', 'apps.course'), namespace='course')),
    path('payinfo/', include(('apps.payinfo.urls', 'apps.payinfo'), namespace='payinfo')),
    path('ueditor/', include(('apps.ueditor.urls', 'apps.ueditor'), namespace='ueditor')),
    # path('search/', include(('apps.search.urls', 'apps.search'), namespace='search')),
    path('search/', include('haystack.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))

