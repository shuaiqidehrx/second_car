# -*- coding:utf-8 -*-
from django.shortcuts import render

# Create your views here.
from alipay import AliPay
from apps.user.models import *
from django.shortcuts import render
from django.views.generic import View
from apps.production.models import Brande,CarStyle
from django.conf import settings
import re
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
import redis
import datetime
from django.db import transaction
from apps.orderform.models import *
from alipay import AliPay
import  os
from django_redis import get_redis_connection
class Create(View):
    @transaction.atomic()
    def post(self,request,count):
        user=request.user
        # 判断登陆
        if not user.is_authenticated():
            return JsonResponse('shit')
        # 取数据
        addressid=request.POST.get('address_id')
        coststyle=request.POST.get('coststyle')
        car_id=request.POST.get('carstyle.id')
        if not all([addressid,coststyle,car_id]):
            return JsonResponse({'info':'数据不完整'})
        try:
            Address.objects.get(id=addressid)
        except Exception as e:
            return JsonResponse({'info':'出错了儿子'})
        # 判断数据是否合法
        # order_id=user.id
        order_id=datetime.now().strftime('%Y%m%d%H%M%S')+str(user.id)+str(car_id)
        save= transaction.savepoint()
        # 设置保存点
        try:
            order=Order.objects.create(
                user=user,
                address=addressid,
                pay_style=coststyle

            )
            # car=CarStyle.objects.get(id=car_id)
            try:
                car=CarStyle.objects.select_for_update().get(id=car_id)
                # 悲观锁
            except Exception as e:
                transaction.savepoint_rollback(save)
                return JsonResponse({'info':'由于商品不存在，所以下单失败'})
            if int(count)>car.count:
                transaction.savepoint_rollback(save)
                return JsonResponse({'info':'超出库存'})
        except Exception as e:
            transaction.savepoint_rollback(save)
            return  JsonResponse({'info':'提交失败了老哥'})
        # 往数据库中进插入
        transaction.savepoint_commit(save)
        # 订单模块
        # orderproduction


def ShowOrder(request):
    return render(request,'orderform/order/订单.html')
class Commit(View):
    def post(self,request):
        # dict1={'0':'支付宝','1':'网银'}
        user=request.user
        carstyle_ids=request.POST.getlist('carstyle_ids')
        if  not carstyle_ids:
            return JsonResponse('')
        adds=Address.objects.filter(user=user)
        totalprice=0
        cn=get_redis_connection()
        key='ord%d'%user.id
        for csid_2 in carstyle_ids:
            carstyle=CarStyle.objects.get(id=csid_2)
            price=carstyle.price
            totalprice=totalprice+price
        context={'adds':adds,'totalprice':totalprice}
        return render(request,'',context)


    def get(self,request,a):
        dict1 = {'0': '支付宝', '1': '网银'}
        if a!=0 & a!=1:
            return JsonResponse({'info':'mistake'})
# 订单模块
# orderproduction
class Cost(View):
    def post(self,request):
        user=request.user
        if not user.is_authenticated():
            return redirect(reverse('user:login'))
        orderid_after=request.POST.get('order_id')
        if not orderid_after:
            return JsonResponse({'info':'订单号不存在'})
        try:
            order=Order.objects.get(id=orderid_after,user=user,pay_style=1,status=0)

        except Exception as  e:
            return JsonResponse({'info':'订单号不存在'})
        # 然后调用支付宝接口
        # 首先完成初始化
        alipay=AliPay(
        appid='2016091400508044',
        app_notify_url=None,
        app_private_key_path=os.path.join(settings.BASE_DIR,'apps/orderform/app_private_key.pem'),
        alipay_public_key_path=os.path.join(settings.BASE_DIR,'apps/orderform/app_public_key.pem'),
        sign_type="RSA2",
        debug=True,

        )
        ord_cost=order.tprice
        # 调用接口
        order_sit=alipay.api_alipay_trade_page_pay(
            subject='花生二手车',
            out_trade_no=orderid_after,
            total_amount=str(ord_cost),
            return_url= None,
            notify_url=None,
        )
        # 支付的时候跳转到做个
        url='https://openapi.alipaydev.com/gateway.do?'+orderid_after
        # 如在真实情况去掉
        return JsonResponse({'info':'准备支付，等待收车','支付地址':url})
# ajax:order_id
class Check(View):
    def post(self,request):
        user=request.user
        if not  user.is_authenticated():
            return JsonResponse({'info':'未登陆'})
        order_id_2=request.POST.get('order_id')
        if not order_id_2:
            return JsonResponse({'info':'没有订单号'})
        try:
            order=Order.objects.get(id=order_id_2,user=user)
        except Exception as e:
            return JsonResponse({'info':'没有订单'})

        alipay = AliPay(
            appid='2016091400508044',
            app_notify_url=None,
            app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/orderform/app_private_key.pem'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/orderform/app_public_key.pem'),
            sign_type="RSA2",
            debug=True,

        )
        while True:
            response=alipay.api_alipay_trade_query(order_id_2)
            code=response.get('code')
            status=response.get('trade_status')
            if code=='10000' and status=='TRADE_SUCCESS':
                order.status=1
                order.save()
                return JsonResponse({'info':'succeed!'})
            elif code=='10000' and status=='WAIT_BUYER_PAY':
                continue
            else:
                return JsonResponse({'info': 'mistake!'})

