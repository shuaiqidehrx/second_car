# -*- coding:utf-8 -*-
from django.db import models
from db.base_model import BaseModel

# Create your models here.

class Order(BaseModel):

    STATUS_CHOICE = (
        (0,'已下单'),
        (1,'已经支付'),
        (2,'配送'),
        (3,'等待手续完成'),
        (4,'完成订单')
    )

    order_id = models.CharField(max_length=50,primary_key=True,verbose_name='订单号')
    user = models.ForeignKey('user.User',verbose_name='买家')
    address = models.ForeignKey('user.Address',verbose_name='买家地址')
    pay_style = models.SmallIntegerField(choices=((0,'贷款'),(1,'支付宝'),(2,'网银')),default=1,verbose_name='支付方式')
    status = models.SmallIntegerField(choices=STATUS_CHOICE,verbose_name='订单完成状态')
    tprice=models.DecimalField(max_digits=20,decimal_places=5,verbose_name='总金额')
    class Meta:
        db_table = 'hs_order'
        verbose_name = '订单详情'
class OrderProduction(BaseModel):
    order=models.ForeignKey('order',verbose_name='订单')
    production=models.ForeignKey('production',verbose_name='产品')
    count=models.IntegerField(default=1,verbose_name='购买数量')
    price=models.DecimalField(max_digits=20,decimal_places=5,verbose_name='车辆价格')
    class Meta:
        db_table='hs_order'
        verbose_name='订单车辆'
        verbose_name_plural=verbose_name