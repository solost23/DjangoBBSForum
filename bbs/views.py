from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from bbs import models
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from bbs import comment_handler
from bbs import form
import json

# Create your views here.

category_list = models.Category.objects.filter(set_as_top_menu=True).order_by("position_index")


def index(request):
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


def acc_login(request):
    if request.method == "POST":
        print(request.POST)
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            # 获取登陆前的页面路径并且重定向，没有则返回到主页
            return HttpResponseRedirect(request.GET.get("next", "/bbs/"))
        else:
            login_err = "Wrong username or password!"
            return render(request, "login.html", {"login_err": login_err})
    return render(request, "login.html")


def acc_logout(request):
    logout(request)
    return HttpResponseRedirect("/bbs/")


def article_detail(request, article_id):
    '''
    文章详情页
    :param request:
    :return: 返回当前文章对象
    '''
    article_obj = models.Article.objects.get(id=article_id)
    # 调用构造树函数
    comment_handler.build_tree(article_obj.comment_set.select_related())
    return render(request, "bbs/article.html", {"article_obj": article_obj,
                                                "category_list": category_list, })


def comment(request):
    if request.method == "POST":
        print(request.POST)
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
    '''
    获取文章评论
    :param request:
    :return:
    '''

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
    '''
    发帖页面,post表示提交文章，get表示返回页面
    :param request:
    :return:
    '''

    # 判断用户有没有登录，如果没有登录，则跳转到登陆页面
    # request.user.is_authenticated
    # 若已经登录，那么允许发帖
    if request.method == "POST":
        # 提交文章内容
        print(request.POST)
        # 图片文件在request.FILES中
        article_form = form.ArticleModelForm(request.POST, request.FILES)
        if article_form.is_valid():
            print(article_form.cleaned_data)
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
    '''
    统计id大于首页第一篇文章的文章数
    :param request:
    :return:
    '''
    latest_article_id = request.GET.get("latest_id")
    if latest_article_id:
        new_article_count = models.Article.objects.filter(id__gt=latest_article_id).count()
        # print("new_article_count", new_article_count)
    else:
        new_article_count = 0
    return HttpResponse(json.dumps({"new_article_count": new_article_count}))


