from django.db import models
import uuid
from customer.models import Customer, Address
from cart.models import Cart
from product.models import Variant

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='customer_orders')
    shipping_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipping_orders'
    )
    billing_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='billing_orders'
    )
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, related_name='order')
    status = models.CharField(max_length=50, default='pending', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ])
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        cart = self.cart

        # get all cart items in the cart
        cart_items = cart.items.all()
        sub_total = 0
        for cart_item in cart_items:
            sub_total += cart_item.variant.price * cart_item.quantity
            
        
        self.sub_total = sub_total
        # self.tax = sub_total * 0.1
        self.tax = 100
        self.shipping_fee = 120
        self.grand_total = sub_total + self.shipping_fee + self.tax
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} for {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # price at order time
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # price at order time

    def save(self, *args, **kwargs):
        self.unit_price = self.variant.price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.variant} in {self.order}"
