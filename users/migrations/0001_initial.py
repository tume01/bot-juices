# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-22 06:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('facebook_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['-created'],
                'default_permissions': ('add', 'change', 'delete', 'get', 'list', 'patch'),
            },
        ),
    ]
