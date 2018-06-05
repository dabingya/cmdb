# -*- coding: utf-8 -*-
# @Time    : 2018/5/24 下午3:10
# @Author  : 大兵

from django.shortcuts import render

def page_not_found(request):
    """
    404 页面
    """
    return render(request,"404.html",{

    })



def page_error(request):
    """
    505 页面
    """
    return render(request, '500.html')