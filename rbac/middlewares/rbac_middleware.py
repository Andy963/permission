#!usr/bin/env python
# *- coding:utf-8 -*-
# Andy Create @ 10/25/2019 9:01 PM
import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse, render, HttpResponse

from rbac.models import Permission


class Auth(MiddlewareMixin):
    def process_request(self, request):
        # pass
        # 登陆白名单
        login_white_list = [reverse('web:login'), ]
        # 权限验证白名单
        # TODO 第一次添加组件时，将 '.*'加入permission_white_list，完成权限的添加
        # if you add '.*/' to permission_white_list, your bread_crumb will not work
        permission_white_list = [reverse('web:index'), '/admin/*', ]

        request.pid = None
        # 默认添加首页的面包屑
        bread_crumb = [{'url': reverse('web:index'), 'title': '首页'}, ]
        request.bread_crumb = bread_crumb
        path = request.path

        if path not in login_white_list:
            # TODO 登陆时可能是username,在login函数中决定
            is_login = request.session.get('is_login')
            if not is_login:
                return redirect('web:login')

            permission_dict = request.session.get('permission_dict')
            for white_path in permission_white_list:
                if re.match(white_path, path):
                    # 在权限白名单，有权限，跳出循环,直接请求页面
                    break
            else:
                # 不在白名单，验证是否对当前路径有权限
                for permission in permission_dict.values():
                    pattern = r'^%s$' % permission['permissions__url']
                    if re.match(pattern, path):
                        # pid 为父级菜单的id,当pid不为None时，说明当前为子菜单，所以先加父级的面包屑，再添加子菜单的面包屑
                        pid = permission.get('permissions__parent_id')
                        if pid:
                            # 添加低级的面包屑
                            request.bread_crumb.append(
                                {'url': permission_dict[str(pid)]['permissions__url'],  # KeyError
                                 'title': permission_dict[str(pid)]['permissions__title'], }
                            )
                            # 添加子菜单面包屑
                            request.bread_crumb.append({
                                'url': permission.get('permissions__url'),
                                'title': permission.get('permissions__title'),
                            })
                            # 此时保存pid为父级菜单的id
                            request.pid = pid
                        else:
                            # 当前父级，不存在子菜单面包屑
                            request.bread_crumb.append({
                                'url': permission.get('permissions__url'),
                                'title': permission.get('permissions__title'),
                            })
                            # 当前为父级菜单时，pid为权限的id
                            request.pid = permission.get('permissions__pk')
                        # 路径匹配成功说明有权限，跳出循环
                        break
                else:
                    # TODO 当没有权限时，作出提示，比如弹框
                    return HttpResponse('权限不足')
