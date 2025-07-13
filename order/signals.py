# orders/signals.py

from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from .models import Order, OrderItem
from decimal import Decimal

@receiver(post_save, sender=Order)
def populate_order_items(sender, instance, created, **kwargs):
    if not created:
        return

    print("populate_order_items")

    def do_stuff():
        cart = instance.cart
        sub_total = 0
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=instance,
                variant=cart_item.variant,
                quantity=cart_item.quantity,
                unit_price=cart_item.variant.price,
                total_price=cart_item.variant.price * cart_item.quantity,
            )
            sub_total += cart_item.variant.price * cart_item.quantity

        # update totals
        instance.sub_total = sub_total
        instance.tax = sub_total * Decimal('0.1')
        instance.shipping_fee = Decimal('120')
        instance.grand_total = sub_total + instance.tax + instance.shipping_fee
        instance.save(update_fields=['sub_total', 'tax', 'shipping_fee', 'grand_total'])
    

    transaction.on_commit(do_stuff)
