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
from django.urls import path
from bbs import views

urlpatterns = [
    path('', views.index, name="bbs"),
    path('category/<int:category_id>/', views.category),
    path('article/<int:article_id>/', views.article_detail, name="article_detail"),
    path('comment/', views.comment, name="post_comment"),
    path('comment_list/<int:article_id>', views.get_comments, name="get_comments"),
    path('new_article/', views.new_article, name="new_article"),
    path('latest_article_count/', views.get_latest_article_count, name="get_latest_article_count"),
]
