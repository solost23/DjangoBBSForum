import json

from django.shortcuts import render, HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required

from bbs import models, comment_handler, form
from DjangoBBSForum.constants import http_method

category_list = models.Category.objects.filter(set_as_top_menu=True).order_by("position_index")


def index(request):
    # 说明要搜索了
    if request.method == http_method.HTTP_POST:
        # print(request.POST)
        keyword = request.POST.get('keyword')
        article_list = models.Article.objects.filter(title__icontains=keyword)
    else:
        # 首页一开始展示全部状态为已发布文章列表
        article_list = models.Article.objects.filter(status="published")
    return render(request, "bbs/index.html", {"category_list": category_list,
                                              "article_list": article_list})


def category(request, category_id):
    category_obj = models.Category.objects.get(id=category_id)
    article_list = models.Article.objects.filter(category_id=category_obj.id, status="published")
    return render(request, "bbs/index.html", {"category_list": category_list,
                                              "category_obj": category_obj,
                                              "article_list": article_list})


# def acc_login(request):
#     if request.method == http_method.HTTP_POST:
#         response = {'user': None, 'msg': None}
#         user = request.POST.get('user')
#         pwd = request.POST.get('pwd')
#         code = request.POST.get('code')
#
#         code_str = request.session.get('code')
#         if code.upper() == code_str.upper():
#             user = authenticate(username=user, password=pwd)
#             if user:
#                 login(request, user)
#                 # 因为是ajax请求，所以不能返回跳转界面什么的，只能返回一个数据
#                 response['user'] = user.username
#             else:
#                 response['msg'] = '用户名或密码错误'
#         else:
#             response['msg'] = 'code error'
#             return JsonResponse(response)
#         return HttpResponseRedirect("/bbs/")
#     return render(request, 'login.html')


# def acc_logout(request):
#     logout(request)
#     return HttpResponseRedirect("/bbs/")


def article_detail(request, article_id):
    """
    文章详情
    """
    article_obj = models.Artricle.objects.get(id=article_id)
    # 调用构造树函数
    comment_handler.build_tree(article_obj.comment_set.select_related())
    return render(request, "bbs/article.html", {"article_obj": article_obj,
                                                "category_list": category_list, })


def comment(request):
    """
    文章评论
    """
    if request.method == http_method.HTTP_POST:
        new_comment_obj = models.Comment(
            article_id=request.POST.get("article_id"),
            parent_comment_id=request.POST.get("parent_comment_id", None),
            comment_type=request.POST.get("comment_type"),
            user_id=request.user.userprofile.id,
            comment=request.POST.get("comment_content"),
        )
        new_comment_obj.save()
        return HttpResponse("success")


def get_comments(request, article_id):
    """
    文章评论
    """
    article_obj = models.Article.objects.get(id=article_id)
    comment_tree = comment_handler.build_tree(article_obj.comment_set.select_related())
    # 手动将评论字典拼接评论成html代码
    tree_html = comment_handler.render_comment_tree(comment_tree)
    return HttpResponse(tree_html)


# 点击发帖默认跳转到/accounts/login/，想修改url有两种方式
# 1.在装饰器后面指定
# @login_required(login_url="/login/")
# 2.在settings.py中指定
@login_required
def new_article(request):
    """
    发帖页面,post表示提交文章，get表示返回页面
    """
    # 判断用户有没有登录，如果没有登录，则跳转到登陆页面
    # request.user.is_authenticated
    # 若已经登录，那么允许发帖
    if request.method == http_method.HTTP_POST:
        # 提交文章内容
        # print(request.POST)
        # 图片文件在request.FILES中
        article_form = form.ArticleModelForm(request.POST, request.FILES)
        if article_form.is_valid():
            # print(article_form.cleaned_data)
            # article_form.cleaned_data是一个属性，不能直接更改，所以要赋给data
            data = article_form.cleaned_data
            data['author_id'] = request.user.userprofile.id

            article_obj = models.Article(**data)
            article_obj.save()

            # article_form.save()
            return HttpResponseRedirect("/bbs/")
        else:
            return render(request, "bbs/new_article.html", {"category_list": category_list,
                                                            "article_form": article_form, })

    # 使用modelForm来展示新建文章表单
    article_form = form.ArticleModelForm()
    return render(request, "bbs/new_article.html", {"category_list": category_list,
                                                    "article_form": article_form, })


def get_latest_article_count(request):
    """
    统计id大于首页第一篇文章的文章数
    """
    latest_article_id = request.GET.get("latest_id")
    if latest_article_id:
        new_article_count = models.Article.objects.filter(id__gt=latest_article_id).count()
        # print("new_article_count", new_article_count)
    else:
        new_article_count = 0
    return HttpResponse(json.dumps({"new_article_count": new_article_count}))


# def register(request):
#     # print(request.POST)
#     # print(request.META)
#     if request.is_ajax():  # 或者可以request.method="POST"
#         # print(request.POST)
#         form = UserForm(request.POST)
#         # 发送ajax一般都返回一个字典
#         response = {'user': None, 'msg': None}
#         if form.is_valid():
#             # print(form.cleaned_data)
#             response['user'] = form.cleaned_data.get('user')
#             # 生成一条用户记录
#             user = form.cleaned_data.get('user')
#             # 为什么user为空？？， 先检查局部钩子，发现后面的变量把前面的变量覆盖掉了，导致返回了一个空
#             # print('user', user)
#             pwd = request.POST.get('pwd')
#             email = request.POST.get('email')
#             avatar_obj = request.FILES.get('avatar')
#             # 判断用户是否上传头像来确定是否走默认值
#             # 进行优化
#             # if avatar_obj:
#             #     user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email, avatar=avatar_obj)
#             # else:
#             #     user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email)
#
#             extra = {}
#             if avatar_obj:
#                 # 字典的键必须和UserInfo中对应才可以赋值
#                 extra['head_img'] = avatar_obj
#             #     传字典用**，非固定参数
#
#             User.objects.create_user(username=user, password=pwd, email=email, **extra)
#         else:
#             # print(form.cleaned_data)
#             # print(form.errors)
#             response['msg'] = form.errors
#         # print(response)
#         return JsonResponse(response)
#
#     form = UserForm()
#     return render(request, 'register.html', locals())


# def get_valid_code_img(request):
#     """
#     获取验证码
#     """
#
#     return HttpResponse(get_code_img(request))


# def not_found(request):
#     return render(request, 'not_found.html')
