from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'customer'

urlpatterns = [
    # Authentication
    path('admin/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='admin_login'),
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='customer:admin_login'), name='admin_logout'),
    
    # Admin dashboard
    path('admin/dashboard/', login_required(views.admin_dashboard), name='admin_dashboard'),
    path('admin/products/', login_required(views.admin_products), name='admin_products'),
    path('admin/orders/', login_required(views.admin_orders), name='admin_orders'),
    path('admin/customers/', login_required(views.admin_customers), name='admin_customers'),
    
    # Redirect from root admin URL to dashboard
    path('admin/', login_required(views.admin_dashboard), name='admin'),
]
