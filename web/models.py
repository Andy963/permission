from django.db import models


# Create your models here.



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


