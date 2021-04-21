from django.contrib import admin
from bbs import models

# Register your models here.
'''
1.注册models(admin.site.register(...))
2.在后台admin中决定展示哪些字段(list_display)
'''


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "pub_date", "last_modify", "status", "priority")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("article", "parent_comment", "comment_type", "comment", "user", "date")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "set_as_top_menu", "position_index")


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.Category, CategoryAdmin)
