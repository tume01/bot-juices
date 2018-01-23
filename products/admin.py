# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ProductCategory, Product, ProductAddonCategory, ProductAddon


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'description',
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'description',
    )

@admin.register(ProductAddonCategory)
class ProductAddonCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'description',
    )

@admin.register(ProductAddon)
class ProductAddonAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'description',
    )