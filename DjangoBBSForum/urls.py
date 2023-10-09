from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from DjangoBBSForum import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bbs/', include("bbs.urls")),
    path('register/', views.register, name="register"),
    path('login/', views.acc_login, name="login"),
    path('logout/', views.acc_logout, name="logout"),
    # 获取验证码
    path('get_validcode_img/', views.get_valid_code_img, name="get_validcode_img"),

    # 所有的都匹配不到走这个
    re_path(r'.*', views.not_found),
]
