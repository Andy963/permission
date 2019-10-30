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
        login_white_list = [reverse('login'), ]
        # 权限验证白名单
        permission_white_list = [reverse('index'), '/admin/*']

        request.pid = None
        bread_crumb = [{'url': reverse('index'), 'title': '首页'}, ]
        request.bread_crumb = bread_crumb
        path = request.path

        if path not in login_white_list:
            is_login = request.session.get('is_login')
            if not is_login:
                return redirect('login')

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
                        pid = permission.get('permissions__parent_id')
                        if pid:
                            # parent_permission = Permission.objects.get(pk=pid)
                            request.bread_crumb.append(
                                {'url': permission_dict[str(pid)]['permissions__url'],  # KeyError
                                 'title': permission_dict[str(pid)]['permissions__title'], }
                            )
                            request.bread_crumb.append({
                                'url': permission.get('permissions__url'),
                                'title': permission.get('permissions__title'),
                            })
                            request.pid = pid
                        else:
                            request.bread_crumb.append({
                                'url': permission.get('permissions__url'),
                                'title': permission.get('permissions__title'),
                            })
                            request.pid = permission.get('permissions__pk')
                        break
                else:
                    return HttpResponse('你不配')
