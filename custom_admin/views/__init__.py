from .views import (
    LoginView, 
    DashboardView, 
    ProductListView, 
    ProductDetailView, 
    CategoryListView,
    CategoryCreateView, 
    BrandCreateView, 
    BrandListView, 
    OrderListView, 
    OrderDetailView,
    CustomerListView, 
    CustomerDetailView, 
    ProductEditView
)
from .api_views import (
    ProductDetailAPI,
    ProductVariantsListCreateAPI,
    ProductVariantDetailAPI,
    BulkUpdateVariantsAPI,
    ProductImagesListCreateAPI,
    ProductImageDetailAPI,
    BulkUpdateImagesAPI
)

__all__ = [
    'LoginView',
    'DashboardView',
    'ProductListView',
    'ProductDetailView',
    'CategoryListView',
    'CategoryCreateView',
    'BrandCreateView',
    'BrandListView',
    'OrderListView',
    'OrderDetailView',
    'CustomerListView',
    'CustomerDetailView',
    'ProductEditView',
    'ProductDetailAPI',
    'ProductVariantsListCreateAPI',
    'ProductVariantDetailAPI',
    'BulkUpdateVariantsAPI',
    'ProductImagesListCreateAPI',
    'ProductImageDetailAPI',
    'BulkUpdateImagesAPI',
]