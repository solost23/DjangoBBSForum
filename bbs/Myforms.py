from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms import widgets
from bbs.models import UserProfile


class UserForm(forms.Form):
    user = forms.CharField(max_length=32, label='用户名',
                           widget=widgets.TextInput(attrs={'class': 'form-control'}),
                           error_messages={'required': '该字段不能为空'})
    pwd = forms.CharField(max_length=32, label='密码',
                          widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                          error_messages={'required': '该字段不能为空'})
    re_pwd = forms.CharField(max_length=32, label='确认密码',
                             widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                             error_messages={'required': '该字段不能为空'})
    email = forms.CharField(max_length=32, label='邮箱',
                            widget=widgets.EmailInput(attrs={'class': 'form-control'}),
                            error_messages={'required': '该字段不能为空'})

    def clean_user(self):
        # user = self.cleaned_data.get('user')
        # 改为val,否则最后user会被覆盖掉，会返回一个空
        val = self.cleaned_data.get('user')
        user = UserProfile.objects.filter(username=val).first()
        if user:
            raise ValidationError('该用户已注册')
        return val

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        # 两个都有值才校验这个，否则直接走上一个错误
        if pwd and re_pwd:
            if pwd != re_pwd:
                # 全局错误保存在__all__中
                raise ValidationError('两次密码不一致')
        return self.cleaned_data
