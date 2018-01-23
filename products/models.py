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
                'title': '{0} - S/.{1}'.format(element.description, round(element.price, 2)),
                'payload': 'PRODUCT_{0}'.format(element.id),
            }
            quick_replies.append(quick_reply)
        return quick_replies

    def to_amount_reply(self, product):
        quick_replies = []
        for index in range(1, 6):
            quick_reply = {
                'title': index,
                'payload': 'AMOUNT_{0}_{1}'.format(index, product.id)
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

    objects = ProductManager()

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS

class ProductAddonCategoryManager(models.Manager):

    def to_quick_reply(self, queryset, order_id):
        quick_replies = []
        for element in queryset:
            quick_reply = {
                'title': element.description,
                'payload': 'ADDON_CATEGORY_{0}_{1}'.format(element.id, order_id),
            }
            quick_replies.append(quick_reply)

        return quick_replies

class ProductAddonCategory(TimeStampedModel):

    objects = ProductAddonCategoryManager()

    product_category = models.ForeignKey(
        'ProductCategory',
        on_delete=models.CASCADE,
        related_name='addon_categories',
    )

    description = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS

class ProductAddonManager(models.Manager):

    def to_quick_reply(self, queryset, order_id):
        quick_replies = []
        for element in queryset:
            quick_reply = {
                'title': element.description,
                'payload': 'ADDON_{0}_{1}'.format(element.id, order_id),
            }
            quick_replies.append(quick_reply)

        return quick_replies

    def more_options_reply(self, product_order_id):
        return [
            {
                'title': 'Si',
                'payload': 'MORE_ADDON_{0}'.format(product_order_id),
            },
            {
                'title': 'No',
                'payload': 'NO_MORE_ADDON_{0}'.format(product_order_id),
            }
        ]

class ProductAddon(TimeStampedModel):

    objects = ProductAddonManager()

    addon_category = models.ForeignKey(
        'ProductAddonCategory',
        on_delete=models.CASCADE,
        related_name='addons',
    )

    description = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS

