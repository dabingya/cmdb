# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 下午1:48
# @Author  : 大兵

from django import forms
from django.forms import fields

class ServerAddForm(forms.Form):
    """
    新增服务器form
    """
    hostname = forms.CharField(max_length=40,required=True,error_messages={
        "required": "请输入主机名"
    })
    remote_ip = forms.GenericIPAddressField(max_length=50,required=True,error_messages={
        "required": "请输入远程连接IP"
    })
    port = forms.IntegerField(required=True,error_messages={
        "required": "请输入连接端口号"
    })
    username = forms.CharField(max_length=20,required=True,error_messages={
        "required": "请输入用户名"
    })
    password = forms.CharField(max_length=50,required=True,error_messages={
        "required": "请输入密码"
    })
    price = forms.FloatField(required=True,error_messages={
        "required": "请输入价格"
    })
    info = forms.CharField(max_length=200,required=False)
    info_secret = forms.CharField(max_length=400,required=False)
    idc = forms.CharField()
    team = forms.CharField()
    account = forms.CharField(required=False)
    env = forms.CharField()
    deadtime = forms.CharField()


class AccountAddForm(forms.Form):
    """
    新增账号form
    """
    name = forms.CharField(max_length=40,required=True,error_messages={
        "required": "请输入账号"
    })
    password = forms.CharField(max_length=50,required=True,error_messages={
        "required": "请输入密码"
    })
    url = forms.URLField(max_length=100,required=True,error_messages={
        "required": "请输入登录地址"
    })
    account_type = forms.CharField()
    info = forms.CharField(max_length=200,required=False)


class LoginForm(forms.Form):
    """
    登录form
    """
    username = forms.CharField(max_length=40,required=True,error_messages={
        "required": "请输入用户名"
    })
    password = forms.CharField(max_length=50, required=True, error_messages={
        "required": "请输入密码"
    })


class AddDomainForm(forms.Form):
    """
    新增域名form
    """
    d_name = forms.CharField(required=True, error_messages={
        "required": "请输入域名"
    })
    resolution = forms.GenericIPAddressField(required=True, error_messages={
        "required": "请输入解析IP"
    })
    account = forms.CharField()
    price = forms.IntegerField(required=True, error_messages={
        "required": "请输入价格"
    })
    date = forms.DateTimeField(required=True, error_messages={
        "required": "请输入到期时间"
    })
    info = forms.CharField(max_length=200,required=False)


class AddConnectForm(forms.Form):
    """
    新增联系人forms
    """
    username = forms.CharField(required=True, error_messages={
        "required": "请输入联系人姓名"
    })
    mobile = forms.IntegerField(required=True,error_messages={
        "required": "请输入手机号码"
    })
    tel = forms.CharField(max_length=20,required=False)
    info = forms.CharField(max_length=200,required=False)



