from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ('title', 'regular_price', 'slug', 'is_active', 'who_created')
  list_filter = ('slug', 'is_active')
