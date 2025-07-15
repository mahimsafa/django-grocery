from django import forms
from django.utils.translation import gettext_lazy as _
from product.models import Category


class BaseAdminForm(forms.ModelForm):
    """Base form class for admin forms with consistent styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Base styling classes
        text_input_class = 'px-1 py-2 block w-full border outline-none rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        textarea_class = 'px-1 py-2 block w-full border outline-none rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        select_class = 'block w-full border outline-none rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
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
        fields = ['name', 'description']
        
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
