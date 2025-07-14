from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy


def admin_login(request):
    """Custom login view for admin"""
    if request.user.is_authenticated:
        return redirect('custom_admin:admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            next_url = request.GET.get('next', reverse_lazy('custom_admin:admin_dashboard'))
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'admin/login.html')


def admin_logout(request):
    """Custom logout view for admin"""
    logout(request)
    return redirect('custom_admin:admin_login')


@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    if not request.user.is_staff:
        return redirect('custom_admin:admin_login')
    return render(request, 'admin/dashboard.html')


@login_required
def admin_products(request):
    """Admin products management view"""
    if not request.user.is_staff:
        return redirect('custom_admin:admin_login')
    return render(request, 'admin/products.html')


@login_required
def admin_orders(request):
    """Admin orders management view"""
    if not request.user.is_staff:
        return redirect('custom_admin:admin_login')
    return render(request, 'admin/orders.html')


@login_required
def admin_customers(request):
    """Admin customers management view"""
    if not request.user.is_staff:
        return redirect('custom_admin:admin_login')
    return render(request, 'admin/customers.html')
