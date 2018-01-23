# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-22 22:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20180122_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlist',
            name='orders',
        ),
        migrations.AddField(
            model_name='order',
            name='order_list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='orders.OrderList'),
            preserve_default=False,
        ),
    ]
