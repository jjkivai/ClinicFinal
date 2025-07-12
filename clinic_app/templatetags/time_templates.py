# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

def ordinal(n):
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

@register.filter
def ordinal_date(value):
    if not value:
        return ''
    return value.strftime(f"%B {ordinal(value.day)}, %Y")
