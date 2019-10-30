#!usr/bin/env python
# *- coding:utf-8 -*-
# Andy Create @ 10/26/2019 4:32 PM
import re
from collections import OrderedDict

from django import template

register = template.Library()

# @register.filter
# def menu(request):
#     menu_list = request.session.get('menu_list')
#     return menu_list

'''
{
    1: {
        'name': '业务系统',
        'icon': 'fa fa-home fa-fw',
        'children': [{
            'title': '客户管理',
            'url': '/customer/list/'
        }],
        'class':''
    },
    2: {
        'name': '财务系统',
        'icon': 'fa fa-jpy fa-fw',
        'children': [{
            'title': '账单管理',
            'url': '/payment/list/'
            'class':'acitve'
        }, {
            'title': '纳税展示',
            'url': '/nashui/'

        }],
        'class':'hidden'
    }
}

'''


@register.inclusion_tag('menu.html')
def menu(request):
    menu_dict = request.session.get('menu_dict')
    menu_order_key = sorted(menu_dict, key=lambda x: menu_dict[x]['weight'], reverse=True)

    menu_order_dict = OrderedDict()

    for key in menu_order_key:
        menu_order_dict[key] = menu_dict[key]

    path = request.path
    for k, v in menu_order_dict.items():
        v['class'] = 'hidden'
        for i in v['children']:
            # if re.match(i['url'], path):
            if request.pid == i['second_menu_id']:
                # print(i['second_menu_id'])
                v['class'] = ''
                i['class'] = 'active'
    menu_data = {'menu_order_dict': menu_order_dict}
    return menu_data
