# Register your models here.
from .models import Cart, CartItem
from django.contrib import admin

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'customer', 'created_at', 'updated_at', 'checked_out')
    search_fields = ('uuid', 'customer__first_name', 'customer__last_name', 'customer__email')
    list_filter = ('checked_out', 'created_at')
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('variant', 'quantity',)
    search_fields = ('cart__uuid', 'variant__name')
    list_filter = ('added_at',)
