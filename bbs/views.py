from django.shortcuts import render
from bbs import models

# Create your views here.

category_list = models.Category.objects.filter(set_as_top_menu=True).order_by("position_index")


def index(request):

    return render(request, "bbs/index.html", {"category_list": category_list})


def category(request, id):
    category_obj = models.Category.objects.get(id=id)
    return render(request, "bbs/index.html", {"category_list": category_list,
                                              "category_obj": category_obj})
