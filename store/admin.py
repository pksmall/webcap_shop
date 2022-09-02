from django.contrib import admin

from .models import Product, Order, Bill


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ('title', 'regular_price', 'slug', 'is_active', 'who_created')
  list_filter = ('slug', 'is_active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ('order_key', 'total_paid', 'created_by', 'created', 'status')
  list_filter = ('created_by', 'status')


admin.site.register(Bill)
