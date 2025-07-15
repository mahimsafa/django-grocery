from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages

from product.models import Product, Category, Brand
from order.models import Order, OrderItem
from .forms import CategoryForm, BrandForm

# Create your views here.

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('custom_admin:dashboard')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('custom_admin:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, self.template_name, {'form': request.POST})

class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('custom_admin:login')

        # Get statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        staff_users = User.objects.filter(is_staff=True).count()
        
        # Get recent activities
        recent_activities = []  # This would typically be your activity log
        
        context = {
            'total_users': total_users,
            'active_users': active_users,
            'staff_users': staff_users,
            'recent_activities': recent_activities,
        }
        
        return render(request, self.template_name, context)

class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 12

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Get related data
        context['variants'] = product.variants.all()
        context['images'] = product.images.all()
        context['category'] = product.category
        context['brand'] = product.brand

        # Get recent orders for this product
        context['recent_orders'] = OrderItem.objects.filter(
            variant__product=product
        ).select_related('order', 'variant').order_by('-order__created_at')[:5]

        return context

class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('custom_admin:categories')

class CategoryListView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'
    paginate_by = 12

class BrandCreateView(CreateView):
    model = Brand
    template_name = 'brand_create.html'
    form_class = BrandForm
    success_url = reverse_lazy('custom_admin:brands')

class BrandListView(ListView):
    model = Brand
    template_name = 'brands.html'
    context_object_name = 'brands'
    paginate_by = 12

class OrderListView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'
    paginate_by = 12
