from django.contrib import admin

# Register your models here.
from .models import Customer, Address
from django.contrib import admin

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('created_at',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'line1', 'city', 'state', 'postal_code', 'country', 'is_default')
    search_fields = ('customer__first_name', 'customer__last_name', 'line1', 'city', 'postal_code')
    list_filter = ('state', 'country', 'is_default')
