from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryListView, CategoryDetailView, BrandListView, BrandDetailView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('brands/<int:id>/', BrandDetailView.as_view(), name='brand-detail'),
]