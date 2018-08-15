# -*- coding:utf-8 -*-
# 全文检索类
from haystack import indexes

from production.models import CarStyle


class carstyleIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return CarStyle

    # 返回模型类
    def index_queryset(self, using=None):
        return self.get_model().objects.all()

#     建立索引数据
