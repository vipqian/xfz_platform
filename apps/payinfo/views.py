from django.shortcuts import render


from .models import PayInfo

from .serializers import PayinfoSerializers
from common import restful
# Create your views here.

def index(request):
    payinfo = PayInfo.objects.all()

    return render(request, 'payinfo/payinfo.html', context={'payinfo': payinfo})


def test(request):
    payinfo = PayInfo.objects.all()
    user = request.user
    if user.is_authenticated:
        serializer = PayinfoSerializers(payinfo,  many=True, context={'author': request.user})
    else:
        serializer = PayinfoSerializers(payinfo, many=True, context={'author': ''})

    return restful.ok(data=serializer.data)

