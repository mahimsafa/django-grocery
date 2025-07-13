from django.contrib import admin
from .models import Product, Variant, ProductImage, Category, Brand

class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'brand__name', 'category__name')
    list_filter = ('brand', 'category', 'created_at')
    inlines = [VariantInline, ProductImageInline]
    prepopulated_fields = {'slug': ('name',)}

    class Media:
        js = ('admin/js/custom_slug.js',)

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price', 'sale_price', 'stock', 'is_active')
    search_fields = ('product__name', 'name', 'sku')
    list_filter = ('is_active', 'product__brand')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_primary')
    search_fields = ('product__name',)
    list_filter = ('is_primary',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')
    search_fields = ('name',)
    list_filter = ('parent',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
