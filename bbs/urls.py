from django.urls import path
from bbs import views

urlpatterns = [
    path('', views.index, name="bbs"),
    path('category/<int:category_id>/', views.category, name='category'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('comment/', views.comment, name='post_comment'),
    path('comment_list/<int:article_id>/', views.get_comments, name='get_comments'),
    path('new_article/', views.new_article, name='new_article'),
    path('latest_article_count/', views.get_latest_article_count, name='get_latest_article_count'),
]
