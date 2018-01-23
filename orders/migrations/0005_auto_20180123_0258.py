# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-23 02:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_productorder_addons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productorder',
            name='comments',
        ),
        migrations.AlterField(
            model_name='productorder',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
