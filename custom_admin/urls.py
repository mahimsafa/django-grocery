from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.urls import reverse_lazy
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Authentication
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    
    # Admin dashboard and management
    path('dashboard/', login_required(views.admin_dashboard), name='admin_dashboard'),
    path('products/', login_required(views.admin_products), name='admin_products'),
    path('orders/', login_required(views.admin_orders), name='admin_orders'),
    path('customers/', login_required(views.admin_customers), name='admin_customers'),
    path('customers/<uuid:customer_id>/', login_required(views.admin_customer_detail), name='admin_customer_detail'),
    path('orders/<uuid:order_id>/', login_required(views.admin_order_detail), name='admin_order_detail'),
    path('products/<int:product_id>/', login_required(views.admin_product_detail), name='admin_product_detail'),
    path('products/<int:product_id>/edit/', login_required(views.admin_product_edit), name='admin_product_edit'),
    
    # Redirect root URL to dashboard if authenticated, otherwise to login
    path('', login_required(views.admin_dashboard), name='admin'),
    
    # Catch-all for login redirects from Django auth
    path('accounts/login/', RedirectView.as_view(url=reverse_lazy('custom_admin:admin_login'), permanent=False)),
]
