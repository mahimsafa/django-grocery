from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from django.views.generic import ListView, CreateView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from product.models import Product, Category
from order.models import Order
from .forms import CategoryForm

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

class OrderListView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'
    paginate_by = 12
