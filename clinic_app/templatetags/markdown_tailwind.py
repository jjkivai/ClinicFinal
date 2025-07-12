import markdown
from bs4 import BeautifulSoup
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def markdownx_tailwind(content):
    if not content:
        return ''
    
    # Convert Markdown to HTML
    html = markdown.markdown(content, extensions=['extra', 'attr_list', 'sane_lists'])
    soup = BeautifulSoup(html, 'html.parser')

    # Add Tailwind classes to specific tags:

    # All h1 tags
    for h1 in soup.find_all('h1'):
        h1['class'] = 'mb-4 text-3xl font-extrabold leading-tight text-gray-900 lg:mb-6 lg:text-4xl dark:text-white'

    # first p tag
    first_p = soup.find('p')
    if first_p:
        first_p['class'] = 'text-lg text-gray-700 mb-6'

    return mark_safe(str(soup))
