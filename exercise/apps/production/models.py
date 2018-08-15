# -*- coding:utf-8 -*-
from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField
from apps.user.models import User

class Brande(BaseModel):
    name = models.CharField(max_length=10,verbose_name='品牌')
    image = models.ImageField(upload_to='xxx',verbose_name='汽车品牌图片')
    intrudcue =HTMLField(blank=True,verbose_name='品牌介绍')

    class Meta:
        db_table = 'hs_brande'
        verbose_name = '汽车品牌'

    def __str__(self):
        return self.name

class CarStyle(BaseModel):
    status = models.IntegerField(choices=((0,'售罄'),(1,'在售')),default=1,verbose_name='车辆在售情况')
    image = models.ImageField(upload_to='xxxx',verbose_name='车辆真实状况')
    deteil = HTMLField(blank=True,verbose_name='车辆情况简介')
    color = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='价格')
    meter = models.IntegerField(verbose_name='里程数')
    brande = models.ForeignKey('Brande',verbose_name='品牌')
    count=models.IntegerField(default=1,verbose_name='库存')
    ower = models.ForeignKey('user.User',verbose_name='拥有者')



    class Meta:
        db_table = 'hs_carstyle'
        verbose_name = '车辆类型'