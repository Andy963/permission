# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-30 08:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_permission_url_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='menus',
        ),
        migrations.RemoveField(
            model_name='permission',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='role',
            name='permissions',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='roles',
        ),
        migrations.DeleteModel(
            name='menu',
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
