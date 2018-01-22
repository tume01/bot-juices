# -*- coding: utf-8 -*-
from model_utils.models import TimeStampedModel
from django.conf import settings
from django_mysql.models import Model
from django.db import models


class ProductCategory(TimeStampedModel):

    description = models.CharField(
        max_length=100,
    )

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS

class Product(TimeStampedModel):

    description = models.CharField(
        max_length=100,
    )

    price = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS
