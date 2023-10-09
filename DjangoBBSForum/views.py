from DjangoBBSForum.utils import valid_code
from DjangoBBSForum.constants import http_method

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User

# 钩子
from bbs.Myforms import UserForm


def register(request):
    # print(request.POST)
    # print(request.META)
    if request.is_ajax():  # 或者可以request.method="POST"
        # print(request.POST)
        form = UserForm(request.POST)
        # 发送ajax一般都返回一个字典
        response = {'user': None, 'msg': None}
        if form.is_valid():
            # print(form.cleaned_data)
            response['user'] = form.cleaned_data.get('user')
            # 生成一条用户记录
            user = form.cleaned_data.get('user')
            # 为什么user为空？？， 先检查局部钩子，发现后面的变量把前面的变量覆盖掉了，导致返回了一个空
            # print('user', user)
            pwd = request.POST.get('pwd')
            email = request.POST.get('email')
            avatar_obj = request.FILES.get('avatar')
            # 判断用户是否上传头像来确定是否走默认值
            # 进行优化
            # if avatar_obj:
            #     user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email, avatar=avatar_obj)
            # else:
            #     user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email)

            extra = {}
            if avatar_obj:
                # 字典的键必须和UserInfo中对应才可以赋值
                extra['head_img'] = avatar_obj
            #     传字典用**，非固定参数

            User.objects.create_user(username=user, password=pwd, email=email, **extra)
        else:
            # print(form.cleaned_data)
            # print(form.errors)
            response['msg'] = form.errors
        # print(response)
        return JsonResponse(response)

    form = UserForm()
    return render(request, 'register.html', locals())


def acc_login(request):
    """
    登录
    """
    if request.method == http_method.HTTP_POST:
        response = {'user': None, 'msg': None}
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        code = request.POST.get('code')

        code_str = request.session.get('code')
        if code.upper() == code_str.upper():
            user = authenticate(username=user, password=pwd)
            if user:
                login(request, user)
                # 因为是ajax请求，所以不能返回跳转界面什么的，只能返回一个数据
                response['user'] = user.username
            else:
                response['msg'] = '用户名或密码错误'
        else:
            response['msg'] = 'code error'
            return JsonResponse(response)
        return HttpResponseRedirect("/bbs/")
    return render(request, 'login.html')


def acc_logout(request):
    """
    注销
    """
    logout(request)
    return HttpResponseRedirect("/bbs/")


def get_valid_code_img(request):
    """
    获取验证码
    """
    return HttpResponse(valid_code.get_code_img(request))


def not_found(request):
    """
    not found页面
    """
    return render(request, 'not_found.html')