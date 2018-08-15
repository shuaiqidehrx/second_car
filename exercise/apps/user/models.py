# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

# Create your models here.


class User(AbstractUser,BaseModel):
    '''
    用户模型的设计与实现
    '''

    nname = models.CharField(max_length=50, verbose_name='昵称', default='')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='male',
                              verbose_name='性别')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    image = models.ImageField(max_length=100, upload_to='xx', default='xxxxx', verbose_name='头像')
    user = models.Manager()
    class Meta:
        db_table = 'hs_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class dm(models.Manager):
    def get_default_address(self,user):
        try:
            add = self.get(user=user,is_default=True)
        except self.model.DoesNotExist:
            add = ''

        return add



class Address(BaseModel):
    user = models.ForeignKey('User',verbose_name='拥有者')
    address = models.CharField(max_length=50,verbose_name='收货地址')
    recieve = models.CharField(max_length=20,verbose_name='收件人')
    phone_nun = models.CharField(max_length=20,verbose_name='联系方式')
    post_num = models.CharField(max_length=6,null=True,verbose_name='邮政编码')
    is_default = models.BooleanField(default=False,verbose_name='默认地址')

    objects = dm()
    class Meta:
        db_table = 'hs_address'
        verbose_name='地址'









