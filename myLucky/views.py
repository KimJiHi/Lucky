import json
import os
import random
import time

from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, response

from myLucky import models
from .models import User, Prize, Attach
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

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
        user.pwd = request.POST.get('pwd')
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


# 登录
@csrf_exempt
def login(request):
    if request.method == "POST":
        acc = request.POST.get('account')
        user = User.objects.get(account=acc)
        token = time.time() + random.randrange(1, 100000)
        user.userToken = str(token)
        user.save()
        request.session['name'] = user.name
        request.session['token'] = user.userToken
        return redirect('/')
    else:
        return render(request, 'mylucky/login.html')


# 验证登录
@csrf_exempt
def checklogin(request):
    acc = request.POST.get('account')
    pwd = request.POST.get('pwd')
    try:
        user = User.objects.get(account=acc, pwd=pwd)
        return JsonResponse({"data": "账号密码正确", "status": "success"})
    except User.DoesNotExist as e:
        return JsonResponse({"data": "密码错误", "status": "error"})


# 主页
def home(request):
    token = request.session.get('token')
    if token is None:
        return redirect('/')
    user = User.objects.get(userToken=token)
    prize = Prize.objects.all()
    # return render(request, 'mylucky/homec.html', {'mine': user.name, 'prize': prize})
    return render(request, 'mylucky/home.html', {'mine': user.name})


from django.core import serializers


# 主页内容
@csrf_exempt
def homelist(request):
    prizes = Prize.objects.all()
    ret = {'status': True, 'data': serializers.serialize('json', prizes)}
    print(ret)
    return HttpResponse(json.dumps(ret))


@csrf_exempt
def dslist(request):
    prizes = Prize.objects.filter(ptype='1')
    ret = {'status': True, 'data': serializers.serialize('json', prizes)}
    print(ret)
    return HttpResponse(json.dumps(ret))


@csrf_exempt
def jrlist(request):
    prizes = Prize.objects.filter(ptype='2')
    ret = {'status': True, 'data': serializers.serialize('json', prizes)}
    print(ret)
    return HttpResponse(json.dumps(ret))


@csrf_exempt
def fhlist(request):
    prizes = Prize.objects.filter(ptype='3')
    ret = {'status': True, 'data': serializers.serialize('json', prizes)}
    print(ret)
    return HttpResponse(json.dumps(ret))


@csrf_exempt
def sjlist(request):
    prizes = Prize.objects.filter(ptype='4')
    ret = {'status': True, 'data': serializers.serialize('json', prizes)}
    print(ret)
    return HttpResponse(json.dumps(ret))


@csrf_exempt
def djlist(request):
    prizes = Prize.objects.filter(ptype='5')
    ret = {'status': True, 'data': serializers.serialize('json', prizes)}
    print(ret)
    return HttpResponse(json.dumps(ret))


def hometype(request, num):
    token = request.session.get('token')
    if token is None:
        return redirect('/')
    user = User.objects.get(userToken=token)
    print(num)
    print(str(num))
    prize = Prize.objects.filter(ptype=str(num))
    return render(request, 'mylucky/home.html', {'mine': user.name, 'prize': prize})


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
from django.contrib import messages


def prize(request, num):
    token = request.session.get('token')
    user = User.objects.get(userToken=token)
    pri = Prize.objects.get(pk=num)
    request.session['prizeID'] = pri.id
    # 获取cookie
    cookies = request.COOKIES.get('prize_list', '')
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
    # 参加抽奖
    if request.method == "POST":
        code = request.POST.get('code')
        if code == pri.code:
            attach = Attach()
            attach.attachUser_id = user.id
            attach.attachPrize_id = pri.id
            attach.save()
            messages.success(request, '参与成功')
            return redirect('/prize/'+str(num)+'/')
        else:
            messages.error(request, '抽奖码错误')
    response = render(request, 'mylucky/prize.html', {'prize': pri, 'joiner': users})
    response.set_cookie('prize_list', cookies)
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
    name = request.session.get('name')

    return render(request, 'mylucky/mine/mine1.html', {'name': name, 'heading': '欢迎'})


def mine2(request, num, ):
    token = request.session.get('token')
    user = User.objects.get(userToken=token)
    cookie = request.COOKIES.get('prize_list')
    if num == 1:
        prize = Attach.objects.filter(attachUser=user.id)
        list = models.Prize.objects.none()
        for i in range(len(prize)):
            list = list | Prize.objects.filter(pk=prize[i].attachPrize_id)
        return render(request, 'mylucky/mine/mine2.html', {'list': list, 'heading': '我参与的'})
    elif num == 2:
        list = Prize.objects.filter(puser_id=user.id)
        return render(request, 'mylucky/mine/mine2.html', {'list': list, 'heading': '我发布的'})
    elif num == 3:
        prize_list = []
        if cookie != '':
            prize_id_list = cookie.split(';')
            for prize_id in prize_id_list:
                if prize_id:
                    list = Prize.objects.get(pk=int(prize_id))
                    prize_list.append(list)
                else:
                    continue
        return render(request,'mylucky/mine/mine2.html',{'list': prize_list,'heading':'历史记录'})



# 退出
from django.contrib.auth import logout


def quit(request):
    logout(request)
    return redirect('/')
