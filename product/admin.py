from django.contrib import admin
from .models import Product, Variant, ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'created_at', 'updated_at')
    search_fields = ('name', 'brand')
    inlines = []

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price', 'stock', 'is_active')
    search_fields = ('product__name', 'name', 'sku')
    list_filter = ('is_active',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_primary')
    search_fields = ('product__name',)
    list_filter = ('is_primary',)
