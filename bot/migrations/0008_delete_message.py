# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-22 04:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_auto_20180122_0427'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]