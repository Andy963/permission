#!usr/bin/env python
# *- coding:utf-8 -*-
# Andy Create @ 10/25/2019 5:34 PM


from django.conf.urls import url
from web.views import customer, payment, auth

urlpatterns = [
    url(r'^login/$', auth.login, name='login'),
    url(r'^index/$', auth.index, name='index'),

    url(r'^customer/list/$', customer.customer_list, name='customer_list'),
    url(r'^customer/add/$', customer.customer_add, name='customer_add'),
    url(r'^customer/edit/(?P<id>\d+)/$', customer.customer_edit, name='customer_edit'),
    url(r'^customer/del/(?P<id>\d+)/$', customer.customer_del, name='customer_del'),
    url(r'^payment/list/$', payment.payment_list, name='payment_list'),
    url(r'^payment/add/$', payment.payment_add, name='payment_add'),
    url(r'^payment/edit/(?P<id>\d+)/$', payment.payment_edit, name='payment_edit'),
    url(r'^payment/del/(?P<id>\d+)/$', payment.payment_del, name='payment_del'),
    url(r'^nashui/$', payment.nashui),
]
