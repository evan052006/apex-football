from django.contrib import admin
from main.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['id']

