import datetime
import json
import os
import random
import time
from django.contrib import messages
from django.db import connection
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, response
from django.template import Context
from django.template.loader import get_template, render_to_string

from myLucky import models
from .models import User, Prize, Attach
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

import hashlib
def password_encrypt(pwd):
    md5 = hashlib.md5()# 2，实例化md5() 方法
    md5.update(pwd.encode())# 3，对字符串的字节类型加密
    result = md5.hexdigest()# 4，加密
    return result

def homepage(request):
    name = request.session.get('name')
    return render(request, 'mylucky/homepage.html', {'user': name})


# 注册
def register(request):
    if request.method == 'POST':
        user = User()
        user.account = request.POST.get('account')
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phoneNumber')
        pwd = request.POST.get('pwd')
        pwd = password_encrypt(pwd)
        user.pwd = pwd
        token = time.time() + random.randrange(1, 100000)
        user.userToken = str(token)
        user.save()
        request.session['name'] = user.name
        request.session['token'] = user.userToken
        return redirect('/')
    else:
        return render(request, 'mylucky/register.html')


# 验证注册
@csrf_exempt
def checkuserid(request):
    userid = request.POST.get("account")
    try:
        user = User.objects.get(account=userid)
        return JsonResponse({"data": "用户名已经被注册", "status": "error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data": "可以注册", "status": "success"})
    pass


# 登录
@csrf_exempt
def login(request):
    if request.method == "POST":
        acc = request.POST.get('account')
        pwd = request.POST.get('pwd')
        pwd = password_encrypt(pwd)
        user = User.objects.get(account=acc)
        if pwd == user.pwd:
            token = time.time() + random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()
            request.session['name'] = user.name
            request.session['token'] = user.userToken
            return redirect('/')
        else:
            messages.error(request, '密码错误')
            return render(request, 'mylucky/login.html')
    else:
        return render(request, 'mylucky/login.html')


# 验证登录
# @csrf_exempt
# def checklogin(request):
#     acc = request.POST.get('account')
#     pwd = request.POST.get('pwd')
#     try:
#         user = User.objects.get(account=acc, pwd=pwd)
#         return JsonResponse({"data": "账号密码正确", "status": "success"})
#     except User.DoesNotExist as e:
#         return JsonResponse({"data": "密码错误", "status": "error"})


# 主页
def home(request):
    token = request.session.get('token')
    if token is None:
        return redirect('/')
    user = User.objects.get(userToken=token)
    # prize = Prize.objects.all().order_by('-id')
    return render(request, 'mylucky/home.html', {'user': user})
    # return render(request, 'mylucky/home.html', {'mine': user.name, 'prize': prize})


from django.core import serializers


# 主页内容
def homelist(request):
    prizes = Prize.objects.filter(isUsed=False).order_by('-id')
    return render(request, 'mylucky/prizeList.html', {'prize': prizes})


def dslist(request):
    prizes = Prize.objects.filter(ptype='1').order_by('-id')
    # ret = {'status': True, 'data': serializers.serialize('json', prizes)}
    # print(ret)
    return render(request, 'mylucky/prizeList.html', {'prize': prizes})


def jrlist(request):
    prizes = Prize.objects.filter(ptype='2').order_by('-id')
    # ret = {'status': True, 'data': serializers.serialize('json', prizes)}
    # print(ret)
    return render(request, 'mylucky/prizeList.html', {'prize': prizes})


def fhlist(request):
    prizes = Prize.objects.filter(ptype='3').order_by('-id')
    # ret = {'status': True, 'data': serializers.serialize('json', prizes)}
    # print(ret)
    return render(request, 'mylucky/prizeList.html', {'prize': prizes})


def sjlist(request):
    prizes = Prize.objects.filter(ptype='4').order_by('-id')
    # ret = {'status': True, 'data': serializers.serialize('json', prizes)}
    # print(ret)
    # return HttpResponse(json.dumps(ret))
    return render(request, 'mylucky/prizeList.html', {'prize': prizes})


def djlist(request):
    prizes = Prize.objects.filter(ptype='5').order_by('-id')
    # ret = {'status': True, 'data': serializers.serialize('json', prizes)}
    # print(ret)
    # return HttpResponse(json.dumps(ret))
    return render(request, 'mylucky/prizeList.html', {'prize': prizes})


#
# def type(request, num):
#     token = request.session.get('token')
#     if token is None:
#         return redirect('/')
#     user = User.objects.get(userToken=token)
#     prize = Prize.objects.filter(ptype=str(num))
#     return render(request, 'mylucky/home.html', {'mine': user.name, 'prize': prize})


# 搜索
@csrf_exempt
def search(request):
    # token = request.session.get('token')
    # user = User.objects.get(userToken=token)
    str = request.POST.get('str')
    list = Prize.objects.filter(Q(name__icontains=str) | Q(puser__name__icontains=str))
    # return render(request, 'mylucky/home.html', {'prize': list, 'mine': user.name})
    return render(request, 'mylucky/prizeList.html', {'prize': list})


import os
from django.conf import settings


# 发布奖品
def release(request):
    token = request.session.get('token')
    user = User.objects.get(userToken=token)
    prize = Prize()
    prize.name = request.POST.get('name')
    prize.ptype = request.POST.get('type')
    prize.num = request.POST.get('num')
    prize.content = request.POST.get('content')
    prize.url = request.POST.get('purl')
    if request.POST.get('img') != '':
        img = request.FILES['img']
        imgurl = os.path.join(settings.PRIZE_IMG, img.name)
        prize.img = os.path.join('prize/img', img.name)
        with open(imgurl, 'wb') as fp:
            for info in img.chunks():
                fp.write(info)
    prize.code = request.POST.get('code')
    prize.usedTime = request.POST.get('usetime')
    prize.puser = user
    prize.save()
    return render(request, 'mylucky/pagejump.html')


# 奖品页
def prize(request, num):
    token = request.session.get('token')
    user = User.objects.get(userToken=token)
    pri = Prize.objects.get(pk=num)
    request.session['prizeID'] = pri.id
    # 历史记录
    # 获取cookie
    cookies = request.COOKIES.get(user.account, '')
    pk = str(pri.id)
    # 如果是第一次浏览，本地没有cookie，直接将id存到cookie里
    if cookies == '':
        cookies = pk + ';'  # ['1','2','3']
    elif cookies != '':
        goods_id_list = cookies.split(';')
        # 判断这个奖品是否已经浏览过
        if pk in goods_id_list:
            goods_id_list.remove(pk)
        goods_id_list.insert(0, pk)
        # 只保留10条记录
        if len(goods_id_list) >= 10:
            goods_id_list = goods_id_list[:10]
        cookies = ';'.join(goods_id_list)
    # 获得参与人员名单
    users = []
    attachs = Attach.objects.filter(attachPrize_id=num)
    for attach in attachs:
        joiner = User.objects.get(pk=attach.attachUser_id)
        users.append(joiner)
    #获得中奖人鱼名单
    luckyUser = []
    luckyAttach = Attach.objects.filter(Q(attachPrize_id=num) & Q(isLucky=True))
    for luckyattach in luckyAttach:
        print(luckyattach.attachPrize.name)
        lucky = User.objects.get(pk=luckyattach.attachUser_id)
        print(lucky.name)
        luckyUser.append(lucky)
    # 参加抽奖
    if request.method == "POST":
        code = request.POST.get('code')
        if code == pri.code:
            attach = Attach()
            attach.attachUser_id = user.id
            attach.attachPrize_id = pri.id
            pri.joinNum+=1
            pri.save()
            attach.save()
            messages.success(request, '参与成功')
            return redirect('/prize/' + str(num) + '/')
        else:
            messages.error(request, '抽奖码错误')
    response = render(request, 'mylucky/prize.html', {'prize': pri, 'joiner': users, 'luckyuser': luckyUser, 'user': user})
    response.set_cookie(user.account, cookies)
    return response


# 验证抽奖
@csrf_exempt
def checkPrize(request):
    token = request.session.get('token')
    user = User.objects.get(userToken=token)
    prizeID = request.session.get('prizeID')
    try:
        attach = Attach.objects.get(attachPrize=prizeID, attachUser=user.id)
        return JsonResponse({"data": "已经参与", "status": "error"})
    except Attach.DoesNotExist as e:
        return JsonResponse({"data": "未参与", "status": "success"})
    pass


# 个人页面
def mine(request):
    token = request.session.get('token')
    user = User.objects.get(userToken=token)
    return render(request, 'mylucky/mine/mine1.html', {'user': user, 'heading': '欢迎你,'})


# 列表分页
from django.core.paginator import Paginator


def mine2(request, num, pageid):
    token = request.session.get('token')
    user = User.objects.get(userToken=token)
    cookie = request.COOKIES.get(user.account)
    if num == 1:
        prize = Attach.objects.filter(attachUser=user.id)
        list = models.Prize.objects.none()
        for i in range(len(prize)):
            list = list | Prize.objects.filter(pk=prize[i].attachPrize_id)
        paginator = Paginator(list, 9)
        page = paginator.page(pageid)
        return render(request, 'mylucky/mine/mine2.html', {'list': page, 'type': 1, 'heading': '我参与的', 'user': user})
    elif num == 2:
        list = Prize.objects.filter(puser_id=user.id)
        paginator = Paginator(list, 9)
        page = paginator.page(pageid)
        return render(request, 'mylucky/mine/mine2.html', {'list': page, 'type': 2, 'heading': '我发布的', 'user': user})
    elif num == 3:
        prize_list = []
        if cookie != None:
            prize_id_list = cookie.split(';')
            for prize_id in prize_id_list:
                if prize_id:
                    list = Prize.objects.get(pk=int(prize_id))
                    prize_list.append(list)
                else:
                    continue
            paginator = Paginator(prize_list, 9)
            page = paginator.page(pageid)
            return render(request, 'mylucky/mine/mine2.html',
                          {'list': page, 'type': 3, 'heading': '历史记录', 'user': user})
        else:
            return render(request, 'mylucky/mine/mine2.html', {'heading': '历史记录', 'type': 3,'user':user})
    elif num == 4:
        prize = Attach.objects.filter(Q(attachUser=user.id) & Q(isLucky=True))
        list = models.Prize.objects.none()
        for i in range(len(prize)):
            list = list | Prize.objects.filter(pk=prize[i].attachPrize_id)
        paginator = Paginator(list, 9)
        page = paginator.page(pageid)
        return render(request, 'mylucky/mine/mine2.html', {'list': page, 'type': 4, 'heading': '我中奖的', 'user': user})

# 个人信息
def mineinfo(request):
    token = request.session.get('token')
    user = User.objects.get(userToken=token)
    if request.method == "POST":
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        pwd = request.POST.get('pwd')
        pwd = password_encrypt(pwd)
        user.pwd = pwd
        if request.POST.get('customFile') != '':
            img = request.FILES['customFile']
            imgurl = os.path.join(settings.USER_IMG, img.name)
            user.img = os.path.join('media/img', img.name)
            with open(imgurl, 'wb') as fp:
                for info in img.chunks():
                    fp.write(info)
        user.save()
        return render(request, 'mylucky/mine/mine3.html', {'user': user})
    return render(request, 'mylucky/mine/mine3.html', {'user': user})


# 退出
from django.contrib.auth import logout


def quit(request):
    logout(request)
    return redirect('/')


from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# 开启定时工作
try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # 设置定时任务，选择方式为interval，时间间隔为10s
    # 另一种方式为每天固定时间执行任务，对应代码为：
    # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
    @register_job(scheduler, "interval", seconds=1)
    def my_job():
        # 这里写你要执行的任务
        now = datetime.datetime.now()
        # print(now)
        prizes = Prize.objects.filter(isUsed=False)
        for prize in prizes:
            if prize.usedTime < now:
                attaches = Attach.objects.filter(attachPrize=prize)
                list = []
                for attach in attaches:
                    list.append(attach.attachUser_id)
                if len(list) == 0:
                    pass
                elif len(list) > int(prize.num):
                    list_fields = random.sample(list, int(prize.num))
                    for list_field in list_fields:
                        luckyUser = User.objects.get(pk=list_field)
                        att = attaches.get(attachUser=luckyUser)
                        att.isLucky = True
                        att.save()
                elif len(list) <= int(prize.num):
                    list_fields = random.sample(list, len(list))
                    for list_field in list_fields:
                        luckyUser = User.objects.get(pk=list_field)
                        att = attaches.get(attachUser=luckyUser)
                        att.isLucky = True
                        att.save()
                prize.isUsed = True
                prize.save()

                    # attachs = Attach.objects.get(attachUser_id=list_field)
                    # print(attachs)
                # prize.isUsed = True

    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()
