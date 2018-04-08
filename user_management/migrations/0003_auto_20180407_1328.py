# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-07 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_auto_20180407_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='is_anonymous',
        ),
        migrations.RemoveField(
            model_name='users',
            name='is_authenticated',
        ),
        migrations.AddField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='users',
            name='password',
            field=models.CharField(default='husain', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]