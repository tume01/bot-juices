# -*- coding: utf-8 -*-
from model_utils.models import TimeStampedModel
from django.conf import settings
from django_mysql.models import Model
from django.db import models

class OrderManager(models.Manager):

    def to_quick_reply(self, queryset):
        quick_replies = []
        return quick_replies

class Order(TimeStampedModel):

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='orders',
    )

    order_list = models.ForeignKey(
        'OrderList',
        on_delete=models.CASCADE,
        related_name='order_details',
    )

    products = models.ManyToManyField('products.Product', through='ProductOrder', related_name='orders')

    objects = OrderManager()

    def total(self):
        total = 0
        for ordered_product in self.orders_detail.all():
                total += ordered_product.amount * ordered_product.product.price
        return total

    @property
    def resume(self):
        print('user')
        resume = '🧞‍♂️ ' + self.user.name + ': {0}'.format(round(self.total(), 2))
        for product_order in self.orders_detail.all():
            resume += '\n' \
                      + product_order.resume
        return resume

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS

class ProductOrder(TimeStampedModel):

    product = models.ForeignKey('products.Product', related_name='orders_detail')
    order = models.ForeignKey('Order', related_name='orders_detail')
    addons = models.ManyToManyField('products.ProductAddon')
    amount = models.IntegerField(default=0)

    @property
    def resume(self):
        resume = '🍰 {0} X {1} = {2}'.format(self.product.description, self.amount, round(self.product.price * self.amount, 2)) \
                + ' \n📋Detalle:'
        for addon in self.addons.all():
            resume += '\n' \
                    + '🔹 ' + addon.addon_category.description + ' - ' + addon.description

        return resume

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS

class OrderList(TimeStampedModel):

    finished = models.BooleanField(default=False)

    def total_amount(self):
        total = 0
        for order in self.order_details.all():
            total += order.total()
        return total

    @property
    def resume(self):
        resume = 'Total: {0}'.format(round(self.total_amount(), 2))
        for order in self.order_details.all():
            resume += '\n' \
                     + order.resume
        return resume

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS



