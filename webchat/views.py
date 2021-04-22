from django.shortcuts import render
from bbs import models
# Create your views here.

category_list = models.Category.objects.filter(set_as_top_menu=True).order_by("position_index")


def dashboard(request):
    '''
    webchat主面板
    :param request:
    :return:
    '''
    # 首页一开始展示全部状态为已发布文章列表
    article_list = models.Article.objects.filter(status="published")
    return render(request, "webchat/dashboard.html", {"category_list": category_list,
                                              "article_list": article_list})









