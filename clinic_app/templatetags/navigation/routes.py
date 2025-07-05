# Description: This file contains the custom template tag to render the navigation links.
from django import template
from django.urls import reverse

# Register the template tag
register = template.Library()

# Define the template tag
@register.inclusion_tag("navigation/navlink.html", takes_context=True)
def render_routes(context):
    request = context.get('request')
    routes = [
        {
            'url': 'clinic_app:home',
            'name': 'Home',
        },
        {
            'url': 'clinic_app:education',
            'name': 'Education',
        },
        {
            'url': 'clinic_app:about-us',
            'name': 'About Us',
        }
    ]

    current_path = request.path if request else None

    for route in routes:
        route['active'] = route['url'] in current_path if current_path else False

    context['routes'] = routes
    return context
