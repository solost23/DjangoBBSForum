from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from bbs import models
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

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
            return render(request, "login.html", {"login_err":login_err})
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
    return render(request, "bbs/article.html", {"article_obj": article_obj,
                                                "category_list": category_list,})


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

