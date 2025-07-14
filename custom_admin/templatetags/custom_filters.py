from django import template

register = template.Library()

@register.filter(name='mul')
def multiply(value, arg):
    """Multiply the value by the arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        try:
            return value * arg
        except Exception:
            return ''
