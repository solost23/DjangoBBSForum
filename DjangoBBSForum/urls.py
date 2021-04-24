"""DjangoBBSForum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from bbs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bbs/', include("bbs.urls")),
    path('login/', views.acc_login, name="login"),
    path('logout/', views.acc_logout, name="logout"),
    path('register/', views.register, name="register"),
    # 获取验证码
    path('get_validcode_img', views.get_validcode_img, name="get_validcode_img"),

    # 所有的都匹配不到走这个
    re_path(r'.*', views.not_found),
]
