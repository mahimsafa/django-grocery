from django.urls import path
from .views import (
    LoginView, 
    DashboardView, 
    ProductListView, 
    ProductDetailView, 
    CategoryListView, 
    BrandListView, 
    OrderListView, 
    OrderDetailView,
    CustomerListView,
    CustomerDetailView,
    CategoryCreateView, 
    BrandCreateView
)

app_name = 'custom_admin'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('brands/', BrandListView.as_view(), name='brands'),
    path('brands/create/', BrandCreateView.as_view(), name='brand_create'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<uuid:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customers/<uuid:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
]