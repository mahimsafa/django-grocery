from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.db.models import Sum, Count, F, Q
from datetime import datetime, timedelta
from decimal import Decimal
from collections import defaultdict

# Import models
from product.models import Product, Variant, Category
from order.models import Order, OrderItem
from customer.models import Customer


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
    
    # Get date ranges for analytics
    today = datetime.now().date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    
    # Calculate total sales
    total_sales = Order.objects.aggregate(
        total=Sum('grand_total')
    )['total'] or Decimal('0')
    
    # Calculate sales for the last 30 days for percentage change
    last_month_sales = Order.objects.filter(
        created_at__date__gte=last_month,
        created_at__date__lte=today
    ).aggregate(total=Sum('grand_total'))['total'] or Decimal('0')
    
    # Calculate sales for the previous 30 days for comparison
    prev_month_start = today - timedelta(days=60)
    prev_month_sales = Order.objects.filter(
        created_at__date__gte=prev_month_start,
        created_at__date__lte=last_month
    ).aggregate(total=Sum('grand_total'))['total'] or Decimal('0')
    
    # Calculate percentage change
    if prev_month_sales > 0:
        sales_change_percentage = ((last_month_sales - prev_month_sales) / prev_month_sales) * 100
    else:
        sales_change_percentage = 100 if last_month_sales > 0 else 0
    
    # Get total orders count
    total_orders = Order.objects.count()
    
    # Get new customers count for the last 30 days
    new_customers = Customer.objects.filter(
        created_at__date__gte=last_month
    ).count()
    
    # Get total products count
    total_products = Product.objects.count()
    
    # Get low stock products (less than 10 in stock)
    low_stock_products = Variant.objects.filter(stock__lt=10).count()
    
    # Get recent orders
    recent_orders = Order.objects.select_related('customer').order_by('-created_at')[:5]
    
    # Get top selling products
    # First, get the top variants by quantity sold
    top_variants = (
        OrderItem.objects
        .values('variant__product')
        .annotate(items_sold=Sum('quantity'))
        .order_by('-items_sold')[:5]
    )
    
    # Get the product IDs from the top variants
    product_ids = [item['variant__product'] for item in top_variants]
    
    # Get the actual product objects in the same order
    top_products = list(Product.objects.filter(id__in=product_ids).prefetch_related('images'))
    
    # Create a dictionary to store the total_sold for each product
    product_sales = {item['variant__product']: item['items_sold'] for item in top_variants}
    
    # Annotate each product with its total_sold
    for product in top_products:
        product.total_sold = product_sales.get(product.id, 0)
    
    # Sort the products by total_sold in descending order
    top_products = sorted(top_products, key=lambda x: x.total_sold, reverse=True)
    
    context = {
        'total_sales': total_sales,
        'sales_change_percentage': sales_change_percentage,
        'total_orders': total_orders,
        'new_customers': new_customers,
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'top_products': top_products,
    }
    
    return render(request, 'admin/dashboard.html', context)


@login_required
def admin_products(request):
    """Admin products management view"""
    if not request.user.is_staff:
        return redirect('custom_admin:admin_login')
    
    # Get search query
    search_query = request.GET.get('q', '')
    
    # Get filter parameters
    category_id = request.GET.get('category')
    in_stock = request.GET.get('in_stock')
    
    # Start with all products
    products = Product.objects.select_related('category', 'brand').prefetch_related('variants')
    
    # Apply search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Apply category filter
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Apply stock filter
    if in_stock == 'in_stock':
        products = products.filter(variants__stock__gt=0)
    elif in_stock == 'out_of_stock':
        products = products.filter(variants__stock=0)
    
    # Get distinct products (in case of variant filtering) and prefetch related data
    products = products.distinct().prefetch_related('variants')
    
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    # Create a list of products with their total stock
    product_list = []
    for product in products:
        total_stock = sum(variant.stock for variant in product.variants.all())
        product_list.append({
            'product': product,
            'total_stock': total_stock,
            'has_low_stock': any(variant.stock < 10 for variant in product.variants.all())
        })
    
    context = {
        'product_list': product_list,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else '',
        'in_stock_filter': in_stock or 'all',
    }
    
    return render(request, 'admin/products.html', context)


@login_required
def admin_orders(request):
    """Admin orders management view"""
    if not request.user.is_staff:
        return redirect('custom_admin:admin_login')
    
    # Get filter parameters
    status = request.GET.get('status', 'all')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    search = request.GET.get('search')
    
    # Start with all orders
    orders = Order.objects.select_related('customer').order_by('-created_at')
    
    # Apply status filter
    if status != 'all':
        orders = orders.filter(status=status)
    
    # Apply date range filter
    if date_from and date_to:
        orders = orders.filter(
            created_at__date__gte=date_from,
            created_at__date__lte=date_to
        )
    
    # Apply search filter
    if search:
        orders = orders.filter(
            Q(id__icontains=search) |
            Q(customer__email__icontains=search) |
            Q(customer__first_name__icontains=search) |
            Q(customer__last_name__icontains=search)
        )
    
    # Get order status choices for filter dropdown
    status_choices = [
        {'value': 'all', 'label': 'All Statuses'},
        *[{'value': choice[0], 'label': choice[1].title()} 
          for choice in Order._meta.get_field('status').choices]
    ]
    
    context = {
        'orders': orders,
        'status_choices': status_choices,
        'current_status': status,
        'date_from': date_from or '',
        'date_to': date_to or '',
        'search_query': search or '',
    }
    
    return render(request, 'admin/orders.html', context)


@login_required
def admin_customers(request):
    """Admin customers management view"""
    if not request.user.is_staff:
        return redirect('custom_admin:admin_login')
    
    # Get search query
    search_query = request.GET.get('q', '')
    
    # Start with all customers
    customers = Customer.objects.all().order_by('-created_at')
    
    # Apply search filter
    if search_query:
        customers = customers.filter(
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Get customer statistics
    total_customers = customers.count()
    new_customers = customers.filter(
        created_at__date__gte=datetime.now().date() - timedelta(days=30)
    ).count()
    
    context = {
        'customers': customers,
        'total_customers': total_customers,
        'new_customers': new_customers,
        'search_query': search_query,
    }
    
    return render(request, 'admin/customers.html', context)
