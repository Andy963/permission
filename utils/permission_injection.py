#!usr/bin/env python
# *- coding:utf-8 -*-
# Andy Create @ 10/28/2019 5:42 PM

from web import models

'''
    {
        # 1-- 一级菜单的id
        1:{
            'name':'业务系统',
            'icon':'fa fa-xx',
            'children':[
                {'title':'客户管理','url':'/customer/list/',},
            ]
        },

        2:{
            'name':'财务系统',
            'icon':'fa fa-xx2',
            'weight':100,
            'children':[
                {'title':'缴费展示','url':'/payment/list/',},

            ]
        }
    }

'''


# 权限注入到session中
def init_permission(request, user_obj):
    # 登录成功之后，将该用户所有的权限(url)全部注入到session中
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
    # request.session['permission_list'] = list(permission_list)  # Object of type 'QuerySet' is not JSON serializable

    menu_dict = {}
    url_names = []
    permission_dict = {}

    for permission in permission_list:
        permission_dict[permission.get('permissions__pk')] = permission
        url_names.append(permission.get('permissions__url_name'))
        if permission.get('permissions__menus__pk'):

            if permission.get('permissions__menus__pk') in menu_dict:
                menu_dict[permission.get('permissions__menus__pk')]['children'].append(
                    {'title': permission.get('permissions__title'),
                     'url': permission.get('permissions__url'),
                     'second_menu_id': permission.get('permissions__pk'),
                     }
                )
            else:
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
    request.session['menu_dict'] = menu_dict
    request.session['url_names'] = url_names
    request.session['permission_dict'] = permission_dict
