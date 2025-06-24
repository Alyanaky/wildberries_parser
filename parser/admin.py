from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_price', 'rating', 'reviews_count', 'category', 'created_at')
    list_filter = ('category', 'rating', 'created_at')
    search_fields = ('name', 'category')