# _*_coding:utf-8_*_
__author__ = 'Solost23'
from django.forms import ModelForm
from bbs import models


class ArticleModelForm(ModelForm):
    class Meta:
        model = models.Article
        exclude = ('author', 'pub_date', 'priority',)

    def __init__(self, *args, **kwargs):
        super(ArticleModelForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]

            field.widget.attrs.update({'class': 'form-control'})
