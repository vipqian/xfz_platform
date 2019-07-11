

from rest_framework import serializers


from .models import PayinfoOrder, PayInfo


class PayinfoSerializers(serializers.ModelSerializer):

    buy = serializers.SerializerMethodField()
    class Meta:
        model = PayInfo
        fields = ['title', 'price', 'profile', 'buy', 'id']


    def get_buy(self, obj):
        author = self.context['author']
        if author:
            buy = PayinfoOrder.objects.filter(payinfo=obj, buyer=author, status=2).exists()
        else:
            buy = False

        return buy