from django.urls import path
from .views import (
    LoginView, 
    DashboardView, 
    ProductListView, 
    ProductDetailView, 
    ProductEditView,
    CategoryListView, 
    BrandListView, 
    OrderListView, 
    OrderDetailView,
    CustomerListView,
    CustomerDetailView,
    CategoryCreateView, 
    BrandCreateView,
    ProductDetailAPI,
    ProductVariantsListCreateAPI,
    ProductVariantDetailAPI,
    BulkUpdateVariantsAPI,
    ProductImagesListCreateAPI,
    ProductImageDetailAPI,
    BulkUpdateImagesAPI
)

app_name = 'custom_admin'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/edit/', ProductEditView.as_view(), name='product_edit'),
    path('api/products/<int:pk>/', ProductDetailAPI.as_view(), name='api_product_detail'),
    path('api/products/<int:product_id>/variants/', ProductVariantsListCreateAPI.as_view(), name='api_variants'),
    path('api/products/<int:product_id>/variants/<int:pk>/', ProductVariantDetailAPI.as_view(), name='api_variant_detail'),
    path('api/products/<int:product_id>/variants/bulk-update/', BulkUpdateVariantsAPI.as_view(), name='api_bulk_update_variants'),
    path('api/products/<int:product_id>/images/', ProductImagesListCreateAPI.as_view(), name='api_images'),
    path('api/products/<int:product_id>/images/<int:pk>/', ProductImageDetailAPI.as_view(), name='api_image_detail'),
    path('api/products/<int:product_id>/images/bulk-update/', BulkUpdateImagesAPI.as_view(), name='api_bulk_update_images'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('brands/', BrandListView.as_view(), name='brands'),
    path('brands/create/', BrandCreateView.as_view(), name='brand_create'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<uuid:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customers/<uuid:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
]