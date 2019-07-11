from django.shortcuts import render
from apps.news.models import News
from django.db.models import Q

# Create your views here.

def index(request):
    p = request.GET.get('title', '')


    if p:
        newses = News.objects.filter(Q(title__icontains=p) | Q(content__icontains=p))
    else:
        newses = News.objects.all()[:2]

    context = {
        'newses': newses,
        'p': p
    }



    return render(request, 'search/search.html', context=context)