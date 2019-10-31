#!usr/bin/env python
# *- coding:utf-8 -*-
# Andy Create @ 10/26/2019 4:32 PM
import re
from collections import OrderedDict

from django import template

register = template.Library()

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
    menu_order_dict = OrderedDict()
    path = request.path

    # 按权重进行排序
    menu_order_key = sorted(menu_dict, key=lambda x: menu_dict[x]['weight'], reverse=True)

    for key in menu_order_key:
        menu_order_dict[key] = menu_dict[key]

    for menu_id, menu in menu_order_dict.items():
        menu['class'] = 'hidden'  # 默认都为折叠状态

        for child_menu in menu['children']:
            # 父级权限的id与某个子菜单id相同时，说明打开的是子菜单，需要展开子菜单，并将其对应的菜单active
            if request.pid == child_menu['second_menu_id']:
                menu['class'] = ''
                child_menu['class'] = 'active'
    menu_data = {'menu_order_dict': menu_order_dict}
    return menu_data


@register.inclusion_tag('bread_crumb.html')
def bread_crumb(request):
    # 从request中获取bread_crumb,渲染到bread_crumb.html,然后返回
    bread_crumb = request.bread_crumb
    context = {'bread_crumb': bread_crumb}
    return context
