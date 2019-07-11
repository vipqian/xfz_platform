# -*- coding: utf-8 -*-#

"""
Name:           search_indexes.py 
# Author:       wangyunfei
# Date:         2019-06-28
# Description:  
"""

from haystack import indexes


from .models import News


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)


    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

