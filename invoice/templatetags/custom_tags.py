from django import template
from django.utils import formats

register = template.Library()

@register.filter
def get_class(value, arg):
    return arg.get(value, 'table-light')

@register.filter
def date_uk(value):
    return formats.date_format(value, "d/m/Y")