from django.urls import path
from .views import LoginView, DashboardView, ProductListView, CategoryListView, OrderListView, CategoryCreateView

app_name = 'custom_admin'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('products/', ProductListView.as_view(), name='products'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('orders/', OrderListView.as_view(), name='orders'),
]