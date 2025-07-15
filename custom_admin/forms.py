from django import forms
from django.utils.translation import gettext_lazy as _
from product.models import Category, Brand, Product, Variant, ProductImage


class BaseAdminForm(forms.ModelForm):
    """Base form class for admin forms with consistent styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Base styling classes
        text_input_class = 'px-1 py-2 block w-full border outline-none rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        textarea_class = 'px-1 py-2 block w-full border outline-none rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        select_class = 'px-1 py-2 block w-full border outline-none rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        checkbox_class = 'rounded outline-none border-gray-300 text-blue-600 focus:border-blue-500 focus:ring-blue-500'
        
        # Apply styling to all fields
        for field in self.fields.values():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': text_input_class})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': textarea_class})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': select_class})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': checkbox_class})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': checkbox_class})
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({'class': checkbox_class})

    def add_placeholder(self, field_name, placeholder_text):
        """Add placeholder text to a specific field"""
        if field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'placeholder': placeholder_text
            })

class CategoryForm(BaseAdminForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder('name', _('Enter category name'))
        self.add_placeholder('description', _('Enter category description'))
        self.fields['description'].widget.attrs.update({'rows': 3})

    def clean_name(self):
        """Custom validation for name field"""
        name = self.cleaned_data.get('name')
        if name and len(name) < 3:
            raise forms.ValidationError(_('Name must be at least 3 characters long'))
        return name

class BrandForm(BaseAdminForm):
    class Meta:
        model = Brand
        fields = ['name', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder('name', _('Enter brand name'))
        self.add_placeholder('description', _('Enter brand description'))
        self.fields['description'].widget.attrs.update({'rows': 3})

class ProductForm(BaseAdminForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'brand']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder('name', _('Enter product name'))
        self.add_placeholder('description', _('Enter product description'))
        self.fields['description'].widget.attrs.update({'rows': 4})

class VariantForm(BaseAdminForm):
    class Meta:
        model = Variant
        fields = ['name', 'sku', 'price', 'sale_price', 'stock', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder('name', _('Enter variant name'))
        self.add_placeholder('sku', _('Enter SKU'))
        self.add_placeholder('price', _('Enter price'))
        self.add_placeholder('sale_price', _('Enter sale price'))
        self.add_placeholder('stock', _('Enter stock quantity'))

class ProductImageForm(BaseAdminForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_primary']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'})
        self.add_placeholder('image', _('Upload product image'))
        self.add_placeholder('is_primary', _('Check it if this is the primary image'))
        self.fields['is_primary'].widget.attrs.update({'class': 'rounded outline-none border-gray-300 text-blue-600 focus:border-blue-500 focus:ring-blue-500'})
        self.add_placeholder('alt_text', _('Enter alt text (optional)'))