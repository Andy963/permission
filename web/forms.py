#!usr/bin/env python
# *- coding:utf-8 -*-
# Andy Create @ 10/25/2019 6:25 PM
# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from web import models


class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class PaymentForm(ModelForm):
    class Meta:
        model = models.Payment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        self.fields['customer'].empty_label = "请选择客户"


class PaymentUserForm(ModelForm):
    class Meta:
        model = models.Payment
        exclude = ['customer', ]

    def __init__(self, *args, **kwargs):
        super(PaymentUserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
