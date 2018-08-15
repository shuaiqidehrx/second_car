# -*- coding:utf-8 -*-
from django.db import models


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False,verbose_name='是否删除')
    create = models.DateTimeField(auto_now_add=True,verbose_name='时间')
    update = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        abstract = True