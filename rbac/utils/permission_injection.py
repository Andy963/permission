#!usr/bin/env python
# *- coding:utf-8 -*-
# Andy Create @ 10/28/2019 5:42 PM

from rbac import models

'''
# menu_dict格式：
{
    1: {
        'name': '业务系统',
        'icon': 'fa fa-home',
        'weight': 100,
        'children': [{
            'title': '客户列表',
            'url': '/customer/list/',
            'second_menu_id': 1
                    }]
        },
    2: {
        'name': '财务系统',
        'icon': 'fa fa-jpy',
        'weight': 100,
        'children ': 
            [{'
            title ': '账单列表 ', '
            url ': ' / payment / list / ', 
            'second_menu_id ': 2
            }]
        },
     4: {
         'name ': '权限管理 ', 
         'icon ': 'fa fa - cubes ',
          'weight ': 100, 
          'children ': 
              [{'title ': '角色展示 ', 
              'url ': ' / role / list / ', 
              'second_menu_id ': 13}, 
              {'title ': '菜单展示 ', 
                'url ': ' / menu / list / ', 
                'second_menu_id ': 16},
              {'title ': '权限展示 ', 
                'url ': ' / permission / list / ',
                'second_menu_id': 17
            }]
        }
}

url_names 其实就是为url起的别名
url_names[
    'customer_list', 
    'payment_list', 
    'customer_add', 
    'customer_edit', 
    'customer_del', 
    'payment_add', 
    'role_add ', 
    'role_list ', 
    'role_edit ', 
    ' role_del ',
    'menu_list ', 
    'permission_list ', 
    ' menu_add ', 
    'menu_edit ', 
    'menu_del '
]

permission dict, 以permission_pk为key
{
    1: {
        'permissions__url': '/customer/list/',
        'permissions__pk': 1,
        'permissions__title': '客户列表 ', 
        'permissions__menus__pk ': 1, 
        'permissions__menus__name ': '业务系统 ', 
        'permissions__menus__icon ': 'fa fa - home', 
        'permissions__menus__weight ': 100, 
        'permissions__parent_id ': None, 
        'permissions__url_name ': 'customer_list '
        },
     2: {
        'permissions__url': '/payment/list/',
        'permissions__pk': 2,
        'permissions__title': '账单列表',
        'permissions__menus__pk ': 2, 
        'permissions__menus__name ': '财务系统 ', 
        'permissions__menus__icon ': 'fa fa - jpy ', 
        'permissions__menus__weight ': 100, 
        'permissions__parent_id ': None, 
        'permissions__url_name ': 'payment_list '
        }, 
}
'''


# 权限注入到session中
def init_permission(request, user_obj):
    # 登录成功之后，将该用户所有的权限(url)全部注入到session中

    menu_dict = {}  # 菜单列表：
    url_names = []  # url别名
    permission_dict = {}  # 权限列表

    # 客户登陆时对当前用户权限进行过滤
    permission_list = models.Role.objects.filter(
        userinfo__username=user_obj.username).values('permissions__url',
                                                     'permissions__pk',
                                                     'permissions__title',
                                                     'permissions__menus__pk',
                                                     'permissions__menus__name',
                                                     'permissions__menus__icon',
                                                     'permissions__menus__weight',
                                                     'permissions__parent_id',
                                                     'permissions__url_name',
                                                     ).distinct()

    for permission in permission_list:
        permission_dict[permission.get('permissions__pk')] = permission

        # 获取所有的权限的别名，在customer_list中对其添加，编辑，删除权限进行判断，
        url_names.append(permission.get('permissions__url_name'))

        # 如果是菜单项，那么需要获取其子菜单
        if permission.get('permissions__menus__pk'):
            # 如果已经添加了，那么向其children中添加子菜单项
            if permission.get('permissions__menus__pk') in menu_dict:
                menu_dict[permission.get('permissions__menus__pk')]['children'].append(
                    {'title': permission.get('permissions__title'),
                     'url': permission.get('permissions__url'),
                     'second_menu_id': permission.get('permissions__pk'),
                     }
                )
            else:
                # 首次添加时，直接将对应的项添加到字典中，组装数据结构
                menu_dict[permission.get('permissions__menus__pk')] = {
                    'name': permission.get('permissions__menus__name'),
                    'icon': permission.get('permissions__menus__icon'),
                    'weight': permission.get('permissions__menus__weight'),
                    'children': [
                        {'title': permission.get('permissions__title'),
                         'url': permission.get('permissions__url'),
                         'second_menu_id': permission.get('permissions__pk'),
                         },
                    ],
                }

    # 依次将菜单，url别名，权限注入到session中
    request.session['menu_dict'] = menu_dict
    request.session['url_names'] = url_names
    request.session['permission_dict'] = permission_dict
