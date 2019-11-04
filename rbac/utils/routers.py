from collections import OrderedDict

from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import RegexURLResolver, RegexURLPattern


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    :param pre_namespace: None
    :param pre_url:  '/'
    :param urlpatterns: []
    :param url_ordered_dict: OrderedDict() 空的有序字典
    :return:
    items :
    <RegexURLResolver <RegexURLPattern list> (admin:admin) ^admin/>
    <RegexURLResolver <module 'web.urls' from '/mnt/d/code/permission/web/urls.py'> (None:None) >
    <RegexURLResolver <module 'rbac.urls' from '/mnt/d/code/permission/rbac/urls.py'> (None:rbac) >
    """

    for item in urlpatterns:
        # 当为另一个url文件时
        if isinstance(item, RegexURLResolver):
            if pre_namespace:
                # pre_namespace默认为None
                if item.namespace:
                    # 当有namespace时，拼接命名空间和别名
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            # 当有命名空间时，将命名空间传入当作pre_namespace递归调用本函数
            recursion_urls(namespace, pre_url + item.regex.pattern, item.url_patterns, url_ordered_dict)
        # 当item为一个视图函数时
        else:
            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name,)
            else:
                # 当没有指定命令空间时，name为item.name即别名
                name = item.name
            if not item.name:
                # 如果别名也没有指定则报错
                raise Exception('URL路由中必须设置name属性')

            url = pre_url + item._regex
            # 最终结果 url_ordered_dict['web:login'] = {'url_name': 'web:login', 'url':'/web/login/'}
            # 通过递归得到所有的url,并加入到字典中
            url_ordered_dict[name] = {'url_name': name, 'url': url.replace('^', '').replace('$', '')}


# router_dict = get_all_url_dict(ignore_namespace_list=['admin', 'rbac'])
def get_all_url_dict(ignore_namespace_list=None):
    """
    获取路由中除去忽略的其它所有路由
    ignore_namespace_list = ['admin', 'rbac']
    :return:
    """
    ignore_list = ignore_namespace_list or []
    url_ordered_dict = OrderedDict()

    # 到得项目的urlpatterns（项目的，非app的） 对象
    md = import_string(settings.ROOT_URLCONF)
    urlpatterns = []


    for item in md.urlpatterns:
        # 当它为RegexURLResolver对象，且别名在忽略列表中时跳过
        if isinstance(item, RegexURLResolver) and item.namespace in ignore_list:
            continue
        urlpatterns.append(item)
    recursion_urls(None, "/", urlpatterns, url_ordered_dict)
    # 当url()第二个参数是callable时，返回的为RegexURLPattern对象
    # 当它为include时，为另一个url文件时，也就是urlpatterns（列表或者元组）则返回 RegexURLResolver对象

    return url_ordered_dict
