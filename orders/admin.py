# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Order, ProductOrder, OrderList


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
    )

@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
    )

@admin.register(OrderList)
class OrderListAdmin(admin.ModelAdmin):

    list_display = (
        'id',
    )