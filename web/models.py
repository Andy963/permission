from django.db import models


# Create your models here.

class menu(models.Model):
    name = models.CharField(max_length=32, verbose_name='菜单标题')
    icon = models.CharField(max_length=32, null=True, blank=True)
    weight = models.IntegerField(default=100)  # 控制菜单排序的,权重值越大,菜单展示越靠前

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '菜单'


class Customer(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.CharField(verbose_name='年龄', max_length=32)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    company = models.CharField(verbose_name='公司', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '客户'


class Payment(models.Model):
    customer = models.ForeignKey(verbose_name='关联客户', to='Customer')
    money = models.IntegerField(verbose_name='付费金额')
    create_time = models.DateTimeField(verbose_name='付费时间', auto_now=True)

    def __str__(self):
        return self.customer.name

    class Meta:
        verbose_name_plural = verbose_name = '账单'


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = verbose_name = '用户'


class Role(models.Model):
    name = models.CharField(max_length=16)
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '角色'


class Permission(models.Model):
    title = models.CharField(max_length=32, verbose_name='路由名称')
    url = models.CharField(max_length=32, verbose_name='url路由')
    menus = models.ForeignKey('Menu', null=True, blank=True, verbose_name='菜单')
    parent = models.ForeignKey('self', null=True, blank=True)
    url_name = models.CharField(max_length=32, null=True, blank=True)  # url的别名

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = verbose_name = '权限'
