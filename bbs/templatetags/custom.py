from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def truncate_url(img_obj):
    # print(dir(img_obj))
    # print(img_obj.name, img_obj.url)
    # 先获取img_url对象的name，即字符串路径，然后在分割
    return "/".join(img_obj.name.split("/")[1:])


@register.simple_tag
def filter_comment(article_obj):
    query_set = article_obj.comment_set.select_related()
    comments = {
        "comment_count": query_set.filter(comment_type=1).count(),
        "thumb_count": query_set.filter(comment_type=2).count()
    }
    return comments

