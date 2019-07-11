# -*- coding: utf-8 -*-#

"""
Name:           serializers 
# Author:       wangyunfei
# Date:         2019-06-13
# Description:  
"""

from rest_framework import serializers
from .models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'telephone', 'username', 'is_active', 'is_staff')
