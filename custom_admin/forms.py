from django import forms
from product.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Text input styling
        text_input_class = 'px-1 py-2 block w-full border outline-none rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        
        # Textarea styling
        textarea_class = 'px-1 py-2 block w-full border outline-none rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        
        # Select styling
        select_class = 'block w-full border outline-none rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        
        # Checkbox styling
        checkbox_class = 'rounded outline-none border-gray-300 text-blue-600 focus:border-blue-500 focus:ring-blue-500'
        
        # Apply styling based on field type
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
                
        # Special handling for specific fields
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter category name'})
        self.fields['description'].widget.attrs.update({
            'rows': 3,
            'placeholder': 'Enter category description'
        })
