# -*- coding:utf-8 -*-
from django.shortcuts import render

# Create your views here.
from alipay import AliPay

from django.shortcuts import render
from django.views.generic import View
from apps.production.models import Brande,CarStyle
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.conf import settings
import re
from django.views.generic import View
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django_redis import get_redis_connection




class AddtionCar(View):
    '''
    完成收藏夹的加入功能
    '''
    def post(self,request):
        user = request.user
    # 完成登录
        if not user.is_authenticated():
            return redirect(reverse('user:login'))

    # 接收数据
        carid_after=request.POST.get('car_id')

    # 校验数据
        if not all([carid_after]):
            return JsonResponse({'info':'数据不完整操作'})

        try:
            car = CarStyle.objects.get(id=carid_after)
        except CarStyle.DoesNotExist:
            return JsonResponse({'info':'您要加入的车辆不存在'})

#     加入到redis数据库里
        cn=get_redis_connection('default')
        key = 'col_%d'%user.id
        cn.lpush(key,carid_after)

        return JsonResponse({'info':'加入收藏成功'})


class ShowCollect(View):
    def get(self,request):
        # 判断登录
        user = request.user
        # 完成登录
        if not user.is_authenticated():
            return redirect(reverse('user:login'))
        # 查询数据(redis数据库)

        cn = get_redis_connection('default')
        key = 'col_%d' % user.id
        values=cn.lrange(key,0,-1)


        # 提取我们所需要的数据

        # 拼接上下文
        # 返回结果


# ajax请求做更新操作
#需要车辆的ID
# update/car_id
# update/1888888/
class UpdateCollect(View):
    def post(self,request):
        # 判断用户是否
        user = request.user
        # 完成登录
        if not user.is_authenticated():
            return JsonResponse({'INFO':'您没有登录，请返回登录'})


        # 接收数据
        carid_after = request.POST.get('car_id')

        # 校验
        # 1 校验是否为空
        if not all([carid_after]):
            return JsonResponse({'INFO': '数据不完整'})
        # 2校验数据的正确性
        try:
            caraf_2 = int(carid_after)
        except Exception as e:
            return JsonResponse({'INFO': '数据错误'})
        # 3 校验是否存在
        try:
            car = CarStyle.objects.get(id=caraf_2)
        except Exception as e:
            return JsonResponse({'INFO': '请求的数据不存在'})

        # 查询数据(redis数据库)
        cn = get_redis_connection('default')
        key = 'col_%d' % user.id


        # 更新
        if car.status == 0:
            '''售罄'''
            return JsonResponse({'INFO':'该车已经卖掉了'})


        # 构造上下文

        # 返回数据
        return JsonResponse({'INFO':'更新成功'})


class DeleteCollect(View):
    def post(self,request):
        # 判断用户是否
        user = request.user
        # 完成登录
        if not user.is_authenticated():
            return JsonResponse({'INFO': '您没有登录，请返回登录'})

        # 接收数据
        carid_after = request.POST.get('car_id')

        # 校验
        # 1 校验是否为空
        if not all([carid_after]):
            return JsonResponse({'INFO': '数据不完整'})
        # 2校验数据的正确性
        try:
            caraf_2 = int(carid_after)
        except Exception as e:
            return JsonResponse({'INFO': '数据错误'})
        # 3 校验是否存在
        try:
            car = CarStyle.objects.get(id=caraf_2)
        except Exception as e:
            return JsonResponse({'INFO': '请求的数据不存在'})

        # 查询数据(redis数据库)
        cn = get_redis_connection('default')
        key = 'col_%d' % user.id
        cn.lrem(key,1,caraf_2)

        return JsonResponse({'INFO': '删除成功'})


def search_car(request):
    return render(request,'serach_pr.html')

