# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
import re
from apps.user.models import User,Address
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

# Paginator
# init
# page(从1开始)
# page_range(从1开始)
# count,num_pages()
#
# Page:
# number
# paginator
# has_next()布尔值
# has_previous
# len()













def register(request):

    if request.method == 'GET':
        # get
        return render(request,'user/register.html')
    elif request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 数据校验
        if not all([username, password, email]):
            return render(request, 'user/register.html', {'info': '数据不完整'})

        if not re.match(r'^1\d{10}$', phone):
            return render(request, 'user/register.html', {'info': '手机号码发生错误'})
        if not re.match(r'^[a-z0-9A-Z]+@(qq|126|163)', email):
            return render(request, 'user/register.html', {'info': '邮箱不正确'})

        # 存储数据
        user = User.objects.create_user(username, password, email)
        user.is_active = 0
        # 激活标志设置为0
        user.save()
        return render(request, 'user/denglu.html')


def register_handle(request):
    #接受数据post
    username=request.POST.get('user_name')
    password = request.POST.get('password')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    #数据校验
    if not all([username,password,email]):
        return render(request,'user/register.html',{'info':'数据不完整'})

    if not re.match(r'^1\d{10}$',phone):
        return render(request, 'user/register.html', {'info': '手机号码发生错误'})
    if not re.match(r'^[a-z0-9A-Z]+@(qq|126|163)',email):
        return render(request, 'user/register.html', {'info': '邮箱不正确'})

    #存储数据
    user=User.objects.create_user(username,password,email)

    return render(request,'user/denglu.html')


class Register(View):
    def get(self,request):
        return render(request,'user/register.html')

    def post(self,request):
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 数据校验
        if not all([username, password, email]):
            return render(request, 'user/register.html', {'info': '数据不完整'})

        if not re.match(r'^1\d{10}$', phone):
            return render(request, 'user/register.html', {'info': '手机号码发生错误'})
        if not re.match(r'^[a-z0-9A-Z]+@(qq|126|163)', email):
            return render(request, 'user/register.html', {'info': '邮箱不正确'})

        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            user=None
        if user:
            return render(request, 'user/register.html', {'info': '用户名已经存在啦'})

        # 存储数据
        user = User.objects.create_user(username=username,password= password, email=email)
        user.is_active = 0
        # 激活标志设置为0
        user.save()
        # 进行激活邮件的设置问题
        # /user/active/id(username,phone,)
        # tr = TR(密钥，过期时间)

        tr = TR(settings.SECRET_KEY,3600)
        dict_active = {'userid':user.id}
        active_info=tr.dumps(dict_active)
        # byte类型

        active_info=active_info.decode()
        print(active_info)

        # 发送邮件
        # send_mail(subject, message, from_email, recipient_list,
        #           fail_silently=False, auth_user=None, auth_password=None,
        #           connection=None, html_message=None):


        # send_active_email(user,active_info)
        subject = '花生二手车，优秀的二手车交易平台'
        message = ''

        from_email = settings.EMAIL_FROM
        reciver = [user.email]
        html_message = '<div>请点击您的激活链接<div><a href="http://127.0.0.1:8000/user/active/%s">屠龙宝刀，点击即送</a>' % active_info
        send_mail(subject, message, from_email, reciver, html_message=html_message)


        print('邮件已经发送')
        return redirect(reverse('production:index'))


class Active(View):
    def get(self,request,active_info):
        tr = TR(settings.SECRET_KEY, 3600)
        try:
            info = tr.loads(active_info)
            userid=info['userid']
            user = User.objects.get(id=userid)
            user.is_active = 1
            user.save()
            return render(request,'user/denglu.html')
        except SignatureExpired as e:
            return HttpResponse('请您重新获取激活链接')



class Login(View):
    def get(self,request):
        if 'password' in request.COOKIES:
            password = request.COOKIES.get('password')
        else:
            password=''

        return render(request,'user/denglu.html',{'password':password})

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remeber')

        if not all([username,password]):
            return render(request,'user/denglu.html',{'info':'数据不完整'})

        user = authenticate(username=username,password=password)
        print(user)
#         自带的登录验证
        if user is not None:
            if user.is_active:
                login(request,user)

                next_url =request.GET.get('next',reverse('production:index'))
                httpresponse = redirect(next_url)

            #    记录登录的状态
            #     httpresponse = HttpResponse('登录成功')
            #     httpresponse=redirect(reverse('user:register'))
                if remember == 'on':
                    httpresponse.set_cookie('username',username)
                else:
                    httpresponse.delete_cookie('username')
                return httpresponse
            else:
                return render(request,'user/denglu.html',{'info':'您的账户未激活'})
        else:
            return render(request, 'user/denglu.html', {'info': '用户名或者密码错误'})



class ProductionShow(View):
    def get(self,request):
        return render(request,'user/chanpin/index.html')


class UserSee(View):
    def get(self,request,page):
        request.user.is_authenticated()
        user=request.user

        cn=get_redis_connection('default')

        key = user.id

        vals=cn.lrange(key,0,100)
        # 分页
        # paginator=Paginator(vals,20)
        #
        # try:
        #     page_new=int(page)
        # except Exception as e:
        #     page_new =1
        #
        #
        # if page_new>paginator.num_pages:
        #     page_new = 1
        #
        # old_page = paginator.page(page_new)
        # # 获取第 page_new的Page对象
        #
        #
        #
        #
        # # 获取对象
        # page=paginator.page()



        return render(request,'user/address.html',{'history':vals})



class Logout(View):
    '''退出操作'''
    def get(self,request):
        logout(request)
        return redirect(reverse('production:index'))


class AddressView(LoginRequired,View):
    def get(self,request):
        user = request.user
        adds=Address.objects.filter(user=user)


        return render(request,'user/address.html',{'addresss':adds})


    def post(self,request):
        #提取数据
        address=request.POST.get('address')
        reciver = request.POST.get('recieve')
        post_num = request.POST.get('post_num')
        phone_num = request.POST.get('phone_num')

        #校验数据
        if not all([address,reciver,phone_num]):
            return render(request, 'user/address.html', {'info': '数据不完整'})


        if not re.match(r'^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\\d{8}$',phone_num):
            return render(request, 'user/register.html', {'info': '电话号码不正确'})

        #存入数据库
        # 第一次输入地址，就是作为我们的默认地址



        user=request.user
        print(request)
#         获取当前用户
#         try:
#             address=Address.objects.get(user=user,is_dafault = True)
#         except Address.DoesNotExist:
#             address=None
        address_object = Address.objects.get_default_address(user=user)
        if address_object:
            is_default = False
        else:
            is_default = True

        Address.objects.create(user=user,recieve=reciver,post_num=post_num,phone_num=phone_num,address=address,is_default=is_default)

        return redirect(reverse('user:address'))






