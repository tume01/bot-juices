# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-17 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_auto_20170917_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='district',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
