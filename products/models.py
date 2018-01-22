# -*- coding: utf-8 -*-
from model_utils.models import TimeStampedModel
from django.conf import settings
from django_mysql.models import Model
from django.db import models

class CategoryManager(models.Manager):

    def to_quick_reply(self, queryset):
        quick_replies = []
        for element in queryset:
            quick_reply = {
                'title': element.description,
                'payload': 'CATEGORY_{0}'.format(element.id),
            }
            quick_replies.append(quick_reply)

        return quick_replies

class ProductCategory(TimeStampedModel):

    description = models.CharField(
        max_length=100,
    )

    objects = CategoryManager()

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS

class ProductManager(models.Manager):

    def to_quick_reply(self, queryset):
        quick_replies = []
        for element in queryset:
            quick_reply = {
                'title': '{0} - S/.{1}'.format(element.description, element.price),
                'payload': 'PRODUCT_{0}'.format(element.id),
            }
            quick_replies.append(quick_reply)

        return quick_replies

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

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='products',
    )

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS
