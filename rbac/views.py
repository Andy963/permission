from django.shortcuts import render, redirect, reverse, HttpResponse
from django.forms import modelformset_factory, formset_factory
from django.db.models import Q

from rbac.models import *
from rbac.forms import *
from rbac.utils.routers import get_all_url_dict


# Create your views here.


def role_list(request):
    role_list = Role.objects.all()
    context = {
        'role_list': role_list,
    }
    return render(request, 'rabc_role_list.html', context)


def role_add_edit(request, id=None):
    role_obj = Role.objects.filter(pk=id).first()
    if request.method == 'GET':
        role_form = RoleModelForm(instance=role_obj)
        return render(request, 'rbac_role_add_edit.html', {'role_form': role_form})
    else:
        role_form = RoleModelForm(request.POST, instance=role_obj)
        if role_form.is_valid():
            role_form.save()
            return redirect('rbac:role_list')
        else:
            return render(request, 'rbac_role_add_edit.html', {'role_form': role_form})


def role_del(request, id):
    models.Role.objects.filter(pk=id).delete()
    return redirect('rbac:role_list')


def menu_list(request):
    menu_id = request.GET.get('mid')
    menu_list = models.Menu.objects.all()

    if menu_id:
        permission_list = models.Permission.objects.filter(Q(menus_id=menu_id) | Q(parent__menus_id=menu_id)).values(
            'id', 'title', 'url', 'url_name', 'menus__id',
            'menus__name', 'menus__icon', 'parent_id')
    else:
        permission_list = models.Permission.objects.all().values('id', 'title', 'url', 'url_name', 'menus__id',
                                                                 'menus__name', 'menus__icon', 'parent_id')

    permission_dict = {}
    for permission in permission_list:
        pid = permission.get('menus__id')
        if pid:
            permission_dict[permission.get('id')] = permission
            permission_dict[permission.get('id')]['children'] = []
    # print(permission_dict)

    for p in permission_list:
        parent_id = p.get('parent_id')
        if parent_id:  # 1
            permission_dict[parent_id]['children'].append(p)

    return render(request, 'rbac_menu_list.html',
                  {'menu_list': menu_list, 'permission_list': permission_dict.values(), 'menu_id': menu_id})


def menu_add_edit(request, id=None):
    menu_obj = models.Menu.objects.filter(pk=id).first()
    if request.method == 'GET':
        menu_form = MenuModelForm(instance=menu_obj)
        return render(request, 'rbac_menu_add_edit.html', {'menu_form': menu_form})
    else:
        menu_form = MenuModelForm(request.POST, instance=menu_obj)
        if menu_form.is_valid():
            menu_form.save()
            return redirect('rbac:menu_list')
        else:
            return render(request, 'rbac_menu_add_edit.html', {'menu_form': menu_form})


def menu_del(request, id):
    models.Menu.objects.filter(pk=id).delete()
    return redirect('rbac:menu_list')


def permission(request, id=None):
    permission_obj = models.Permission.objects.filter(id=id).first()
    permission_form = PermissionForm(instance=permission_obj)
    if request.method == 'POST':
        permission_form = PermissionForm(request.POST, instance=permission_obj)
        if permission_form.is_valid():
            permission_form.save()
            return redirect(reverse('rbac:permission_list'))

    return render(request, 'rbac_menu_add_edit.html', {'menu_form': permission_form})


def del_permission(request, id):
    models.Permission.objects.filter(id=id).delete()
    return redirect(reverse('rbac:permission_list'))


def permission_list(request):
    """
    批量操作权限
    :param request:
    :return:
    """

    post_type = request.GET.get('type')

    # 更新和编辑用的
    FormSet = modelformset_factory(models.Permission, MultiPermissionForm, extra=0)
    # 增加用的
    AddFormSet = formset_factory(MultiPermissionForm, extra=0)

    permissions = models.Permission.objects.all()

    # 获取路由系统中所有URL
    router_dict = get_all_url_dict(ignore_namespace_list=['admin', ])

    # 数据库中的所有权限的别名
    permissions_name_set = set([i.url_name for i in permissions])

    # 路由系统中的所有权限的别名
    router_name_set = set(router_dict.keys())

    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]

            query_list = models.Permission.objects.bulk_create(permission_obj_list)

            for i in query_list:
                permissions_name_set.add(i.url_name)

    add_name_set = router_name_set - permissions_name_set
    add_formset = AddFormSet(initial=[row for name, row in router_dict.items() if name in add_name_set])

    del_name_set = permissions_name_set - router_name_set
    del_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=del_name_set))

    update_name_set = permissions_name_set & router_name_set
    update_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset.save()
            update_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=update_name_set))

    context = {
        'del_formset': del_formset,
        'update_formset': update_formset,
        'add_formset': add_formset,
    }
    return render(request, 'rbac_permission_list.html', context)


def permission_dispatch(request):
    """
    分配权限
    :param request:
    :return:
    """

    uid = request.GET.get('uid')  # 1
    rid = request.GET.get('rid')  # 1

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        user = UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        user.roles.set(request.POST.getlist('roles'))

    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role = Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permissions.set(request.POST.getlist('permissions'))

    # 查询所有用户
    user_list = UserInfo.objects.all()
    # 查询用户对应的id和角色
    user_has_roles = UserInfo.objects.filter(id=uid).values('id', 'roles')

    user_has_roles_dict = {item['roles']: None for item in user_has_roles}
    # {1:None,3:None}  #1和3是用户对应的角色id的值
    # if a in user_has_roles_dict:

    """
    用户拥有的角色id
    user_has_roles_dict = { 角色id：None }
    """
    # 获取所有角色
    role_list = Role.objects.all()

    if rid:
        role_has_permissions = Role.objects.filter(id=rid).values('id', 'permissions')
    elif uid and not rid:
        user = UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.values('id', 'permissions')
    else:
        role_has_permissions = []
    # role_has_permissions 看用户所有角色对应的所有权限

    role_has_permissions_dict = {item['permissions']: None for item in role_has_permissions}

    """
    角色拥有的权限id
    role_has_permissions_dict = { 权限id：None }
    """

    all_menu_list = []  # 最终要做的数据结构就存在这里面

    queryset = Menu.objects.values('id', 'name')  # 一级菜单数据
    # queryset = [{'id':1,'name':'业务系统','children':[]},{'id':2,'name':'财务系统','children':[]}]

    menu_dict = {}
    '''
    menu_dict = {
        一级菜单id--1：{'id':1,'name':'业务系统','children':[
            {id:1,'title':'客户展示','menus_id':1,'children':[
                {'id':1,'title':'添加客户','parent_id':1},
                {'id':2,'title':'编辑客户','parent_id':1},
            ]},
            {id:2,'title':'缴费展示','menus_id':2,'children':[]},

        ]}，
        一级菜单id--2：{'id':2,'name':'财务系统','children':[]}，
        没有分配菜单的权限--None：{'id': None, 'name': '其他', 'children': []}
    }
    all_menu_list = [
        {'id':1,'name':'业务系统','children':[
            {id:1,'title':'客户展示','menus_id':1,'children':[
                {'id':1,'title':'添加客户','parent_id':1},
                {'id':2,'title':'编辑客户','parent_id':1},
            ]},
            {id:2,'title':'缴费展示','menus_id':2,'children':[]},
        ]},
        {'id':2,'name':'财务系统','children':[]},
        {'id': None, 'name': '其他', 'children': []}
    ]
    '''

    for item in queryset:
        item['children'] = []  # 放二级菜单，父权限
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id': None, 'name': '其他', 'children': []}
    all_menu_list.append(other)
    menu_dict[None] = other

    # 二级菜单权限数据
    root_permission = Permission.objects.filter(menus__isnull=False).values('id', 'title', 'menus_id')
    # [{id:1,'title':'客户展示','menus_id':1,'children':[]},{id:1,'title':'缴费展示','menus_id':2,'children':[]}]
    root_permission_dict = {}

    """
    root_permission_dict = {
        二级菜单id--1：{id:1,'title':'客户展示','menus_id':1,'children':[
            {'id':1,'title':'添加客户','parent_id':1},
            {'id':2,'title':'编辑客户','parent_id':1},
        ]},
        二级菜单id--2：{id:2,'title':'缴费展示','menus_id':2,'children':[]},

    }
    """

    for per in root_permission:
        per['children'] = []  # 放子权限
        nid = per['id']  # 二级菜单id值
        menu_id = per['menus_id']  # 一级菜单id值  -- 1
        root_permission_dict[nid] = per
        menu_dict[menu_id]['children'].append(per)

    # 二级菜单的子权限
    node_permission = Permission.objects.filter(menus__isnull=True).values('id', 'title', 'parent_id')
    # [{'id':1,'title':'添加客户','parent_id':1},{'id':2,'title':'编辑客户','parent_id':1},]
    for per in node_permission:
        pid = per['parent_id']  # pid 对应的二级菜单的id
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)

    context = {
        'user_list': user_list,
        'role_list': role_list,
        'user_has_roles_dict': user_has_roles_dict,
        'role_has_permissions_dict': role_has_permissions_dict,
        'all_menu_list': all_menu_list,
        'uid': uid,
        'rid': rid
    }

    return render(request, 'rbac_permission_dispatch.html', context)
