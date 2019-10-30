#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect

from web import models
from web.forms import PaymentForm, PaymentUserForm


def nashui(request):
    pass

def payment_list(request):
    """
    付费列表
    :return:
    """
    data_list = models.Payment.objects.all()
    return render(request, 'payment_list.html', {'data_list': data_list})


def payment_add(request):
    """
    编辑付费记录
    :return:
    """
    if request.method == 'GET':
        form = PaymentForm()
        return render(request, 'payment_edit.html', {'form': form})
    form = PaymentForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/payment/list/')
    return render(request, 'payment_edit.html', {'form': form})


def payment_edit(request, id):
    """
    新增付费记录
    :return:
    """
    obj = models.Payment.objects.get(id=id)
    if request.method == 'GET':
        form = PaymentForm(instance=obj)
        return render(request, 'payment_add.html', {'form': form})
    form = PaymentForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/payment/list/')
    return render(request, 'payment_add.html', {'form': form})


def payment_del(request, id):
    """
    删除付费记录
    :param request:
    :param cid:
    :return:
    """
    models.Payment.objects.filter(id=id).delete()
    return redirect('/payment/list/')

