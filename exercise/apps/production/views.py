# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from apps.production.models import Brande,CarStyle
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
import re
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from itsdangerous import TimedJSONWebSignatureSerializer as TR
from itsdangerous import SignatureExpired
from django.core.mail import send_mail
# from django.shortcuts import redirect
from celery_task.tasks import send_active_email
from django.core.urlresolvers import reverse
from utils.mixin import LoginRequired
# from redis import StrictRedis
from django_redis import get_redis_connection
from django.core.paginator import Paginator,Page
# 127.0.0.1:8000/user/register

# Create your views here.



class Index(View):
    def get(self,request):
        return render(request, 'production/index/index.html')


class Detail(View):
    def get(self,request,c_id):
        try:
            car = CarStyle.objects.get(id=c_id)
        except CarStyle.DoesNotExist:
            return render(request, 'production/index/index.html')

        user=request.user

        if user.is_authenticated():
            cn = get_redis_connection('default')
            key = user.id
            val = car.id
            cn.lpush(key,val)
            cn.ltrim(key,0,19)
            # user_id:[9,7,5]

        else:
            return redirect(reverse('user:login'))

        context ={
            'carstyle':car
        }


        return render(request,'production/detail.html',context)



class ShowAllCar(View):
    def get(self,request,b_id,page):
        '''展示该品牌所有的车辆信息'''
        try:
            brande_after = Brande.objects.get(id=b_id)

        except Brande.DoesNotExist:
            return redirect(reverse('production:index'))


#         找到排序方式
        sort=request.GET.get('sort')
# 根据排序方式，找到并取出数据
        if sort == 'default':
            car_list = CarStyle.objects.filter(brande=brande_after).order_by('id')
        elif sort == 'newest':
            car_list = CarStyle.objects.filter(brande=brande_after).order_by('create')
        elif sort == 'price':
            pass
        elif sort == 'meter':
            pass
        else:
            return redirect(reverse('production:index'))


# 进行分页处理
        paginator = Paginator(car_list,20)

        try:
            page_after = int(page)
        except Exception as e:
            page_after = 1


        numpage_after=paginator.num_pages
#         分页所得的最大页码数
#         总共展示7条数据
        if numpage_after <7:
            pages = range(1,numpage_after+1)

        else:
            if page_after <4:
                pages = range(1,8)

            elif numpage_after - page_after < 3:
                pages = range(numpage_after-6,numpage_after+1)

            else:
                pages = range(page_after-3,page_after+4)

        context = {
            'page_after':page_after,
            'brande_after':brande_after,
            'car_list':car_list,
            'sort':sort
        }
        return render(request,'production/list_show.html',context)

#
# class Search(View):
#     def get(self,request):
#         sql = 'select * from hs_carstyle where brande like 大众'
#         大众：








