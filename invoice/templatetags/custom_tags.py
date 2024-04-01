from django import template
from django.utils import formats

register = template.Library()

@register.filter
def get_class(value, arg):
    return arg.get(value, 'table-light')

@register.filter
def date_uk(value):
    return formats.date_format(value, "d/m/Y")

@register.filter
def format_currency(value, currency='£'):
    pounds_value = value / 100
    format_pounds = number_format(pounds_value, decimal_pos=2, force_grouping=True)
    return f'{currency}{format_pounds}'