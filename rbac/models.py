from django.db import models


# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=32, verbose_name='菜单标题')
    icon = models.CharField(max_length=32, null=True, blank=True, verbose_name='图标')
    weight = models.IntegerField(default=100, verbose_name='权重')  # 控制菜单排序的,权重值越大,菜单展示越靠前

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '菜单'


class UserInfo(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    roles = models.ManyToManyField('Role')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = verbose_name = '用户'


class Role(models.Model):
    name = models.CharField(max_length=16,verbose_name='角色名')
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '角色'


class Permission(models.Model):
    title = models.CharField(max_length=32, verbose_name='权限名称')
    url = models.CharField(max_length=32, verbose_name='路由路径')
    menus = models.ForeignKey('Menu', null=True, blank=True, verbose_name='菜单')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name='父级菜单')
    url_name = models.CharField(max_length=32, null=True, blank=True, verbose_name='路由别名')  # url的别名

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = verbose_name = '权限'
