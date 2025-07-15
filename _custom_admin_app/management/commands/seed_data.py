import os
import random
import uuid
from datetime import datetime, timedelta
from django.utils.text import slugify
from django.core.management.base import BaseCommand
from faker import Faker
from product.models import Category, Brand, Product, ProductImage, Variant
from customer.models import Customer, Address
from cart.models import Cart, CartItem
from order.models import Order

# Set up Faker
fake = Faker()

# Sample data
CATEGORIES = [
    'Fruits', 'Vegetables', 'Dairy', 'Meat', 'Bakery', 'Beverages', 'Snacks',
    'Frozen Foods', 'Canned Goods', 'Grains', 'Spices', 'Sauces', 'Breakfast',
    'Desserts', 'Seafood', 'Poultry', 'Organic', 'Gluten Free'
]

BRANDS = [
    'Farm Fresh', 'Nature\'s Best', 'Organic Valley', 'Happy Farms', 'Green Fields',
    'Golden Harvest', 'Pure Life', 'Healthy Choice', 'Tasty Bites', 'Ocean\'s Finest'
]

PRODUCT_NAMES = [
    'Apple', 'Banana', 'Orange', 'Milk', 'Eggs', 'Bread', 'Chicken Breast',
    'Ground Beef', 'Salmon Fillet', 'Rice', 'Pasta', 'Tomato Sauce', 'Cheese',
    'Yogurt', 'Butter', 'Lettuce', 'Tomatoes', 'Potatoes', 'Onions', 'Garlic',
    'Carrots', 'Broccoli', 'Spinach', 'Strawberries', 'Blueberries', 'Grapes',
    'Cereal', 'Oatmeal', 'Honey', 'Olive Oil', 'Vinegar', 'Salt', 'Pepper',
    'Sugar', 'Flour', 'Chocolate', 'Cookies', 'Ice Cream', 'Frozen Pizza',
    'Frozen Vegetables', 'Canned Beans', 'Canned Tuna', 'Peanut Butter', 'Jam',
    'Coffee', 'Tea', 'Juice', 'Soda', 'Water', 'Chips', 'Nuts'
]

VARIANT_TYPES = {
    'weight': ['100g', '250g', '500g', '1kg', '2kg', '5kg'],
    'volume': ['250ml', '500ml', '1L', '2L', '5L'],
    'count': ['1pc', '3pcs', '6pcs', '12pcs'],
    'size': ['Small', 'Medium', 'Large', 'Extra Large']
}

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate database...')
        
        # Create categories
        self.stdout.write('Creating categories...')
        categories = []
        for cat_name in CATEGORIES:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            categories.append(category)
        
        # Create brands
        self.stdout.write('Creating brands...')
        brands = []
        for brand_name in BRANDS:
            brand, created = Brand.objects.get_or_create(
                name=brand_name,
                defaults={'description': f"Premium quality {brand_name} products"}
            )
            brands.append(brand)
        
        # Create products
        self.stdout.write('Creating products...')
        products = []
        for i in range(50):
            product = Product.objects.create(
                name=f"{random.choice(PRODUCT_NAMES)} {fake.word().capitalize()}",
                description=fake.paragraph(nb_sentences=3),
                brand=random.choice(brands),
                category=random.choice(categories)
            )
            products.append(product)
            
            # Create variants for each product
            variant_type = random.choice(list(VARIANT_TYPES.keys()))
            variant_values = VARIANT_TYPES[variant_type]
            
            for value in variant_values:
                price = round(random.uniform(1, 100), 2)
                Variant.objects.create(
                    product=product,
                    name=value,
                    price=price,
                    sale_price=round(price * random.uniform(0.7, 0.95), 2) if random.random() > 0.3 else None,
                    stock=random.randint(0, 1000),
                    sku=f"SKU-{product.id}-{value}",
                    is_active=random.random() > 0.1  # 90% chance of being active
                )
        
        # Create customers
        self.stdout.write('Creating customers...')
        customers = []
        for _ in range(20):
            customer = Customer.objects.create(
                email=fake.unique.email(),
                phone=fake.phone_number()[:20],
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            
            # Create 1-3 addresses per customer
            for _ in range(random.randint(1, 3)):
                is_default = not customer.addresses.exists()  # First address is default
                Address.objects.create(
                    customer=customer,
                    line1=fake.street_address(),
                    line2=fake.secondary_address() if random.random() > 0.7 else '',
                    city=fake.city(),
                    state=fake.state(),
                    postal_code=fake.postcode(),
                    country=fake.country(),
                    is_default=is_default
                )
            customers.append(customer)
        
        # Create carts and cart items
        self.stdout.write('Creating carts and items...')
        selected_customers = random.sample(customers, 8)
        all_variants = list(Variant.objects.all())
        
        for customer in selected_customers:
            # Each customer gets 1-2 carts
            for _ in range(random.randint(1, 2)):
                cart = Cart.objects.create(
                    customer=customer,
                    checked_out=random.random() > 0.3  # 70% chance of being checked out
                )
                
                # Add 1-5 items to each cart
                for _ in range(random.randint(1, 5)):
                    variant = random.choice(all_variants)
                    CartItem.objects.create(
                        cart=cart,
                        variant=variant,
                        quantity=random.randint(1, 5)
                    )
                
                # If cart is checked out, create an order
                if cart.checked_out:
                    addresses = list(customer.addresses.all())
                    shipping_address = random.choice(addresses)
                    billing_address = random.choice(addresses)
                    
                    # Calculate cart total
                    subtotal = sum(
                        item.variant.price * item.quantity 
                        for item in cart.items.all()
                    )
                    from decimal import Decimal
                    shipping_fee = Decimal(str(round(random.uniform(5, 20), 2)))
                    tax = round(subtotal * Decimal('0.1'), 2)  # 10% tax
                    
                    Order.objects.create(
                        customer=customer,
                        shipping_address=shipping_address,
                        billing_address=billing_address,
                        cart=cart,
                        status=random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
                        sub_total=subtotal,
                        shipping_fee=shipping_fee,
                        tax=tax,
                        grand_total=subtotal + shipping_fee + tax
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))