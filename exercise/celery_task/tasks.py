# -*- coding:utf-8 -*-
# main.py
from celery  import Celery
from django.conf import settings
from django.core.mail import send_mail
# 第二台电脑执行的操作
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "huashengcar.settings")
# django.setup()


#创建一个celery对象
app = Celery('celery_task.tasks',broker='redis://127.0.0.1:6379')


@app.task
def send_active_email(user,active_info):
    # 创建任务
    subject = '花生二手车，优秀的二手车交易平台'
    message = '您好，这是激活邮件'
    message = message.encode('utf-8')
    from_email = settings.EMAIL_FROM
    reciver = [user.email]
    html_message = '<div>请点击您的激活链接<div><a href="http://127.0.0.1:8000/user/active/%s">屠龙宝刀，点击即送</a>' % active_info
    send_mail(subject, message, from_email, reciver, html_message=html_message)