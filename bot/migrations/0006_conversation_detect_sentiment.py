# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-17 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20170917_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='detect_sentiment',
            field=models.NullBooleanField(),
        ),
    ]
