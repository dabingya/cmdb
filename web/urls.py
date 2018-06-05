# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 下午1:46
# @Author  : 大兵



from django.conf.urls import url
from django.views.generic import TemplateView
from web.views import ServerView,ServerDetailView,AddServerView,AccountView,\
    DomainView,ConnectView,ServerEditView,UpdateDataView,AddAccountView,AccountEditView,\
    LoginView,IndexView,AddDomainView,EditDomainView,AddConnectView,EditConnectView,Lgout

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    # 登录
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'index/$', IndexView.as_view(), name='index'),
    url(r'lgout/$', Lgout.as_view(), name='lgout'),

    # 服务器
    url(r'^server/$',ServerView.as_view(),name='server'),
    url(r'^server-detail/(?P<id>\d+)$',ServerDetailView.as_view(),name='server-detail'),
    url(r'^edit-server/(?P<idd>\d+)$',ServerEditView.as_view(),name='server-edit'),
    url(r'^add-server/$',AddServerView.as_view(),name='add-server'),

    # 账号
    url(r'^account/$',AccountView.as_view(),name='account'),
    url(r'^add-account/$',AddAccountView.as_view(),name='add-account'),
    url(r'^edit-account/(?P<id>\d+)$',AccountEditView.as_view(),name='account-edit'),

    # 域名
    url(r'^domain/$',DomainView.as_view(),name='domain'),
    url(r'^add-domain/$',AddDomainView.as_view(),name='add-domain'),
    url(r'^edit-domain/(?P<id>\d+)$',EditDomainView.as_view(),name='domain-edit'),

    # 联系人管理
    url(r'^connect/$',ConnectView.as_view(),name='connect'),
    url(r'^add-connect/$',AddConnectView.as_view(),name='add-connect'),
    url(r'^edit-connect/(?P<id>\d+)$',EditConnectView.as_view(),name='connect-edit'),


    # 更新数据
    url(r'^update/$',UpdateDataView.as_view(),name="update_data")
]

