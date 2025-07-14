from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.

@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    return render(request, 'admin/dashboard.html')

@login_required
def admin_products(request):
    """Admin products management view"""
    return render(request, 'admin/products.html')

@login_required
def admin_orders(request):
    """Admin orders management view"""
    return render(request, 'admin/orders.html')

@login_required
def admin_customers(request):
    """Admin customers management view"""
    return render(request, 'admin/customers.html')
