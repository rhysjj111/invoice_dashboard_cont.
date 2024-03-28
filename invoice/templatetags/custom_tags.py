from django import template

register = template.Library()

@register.filter
def get_class(value, arg):
    return arg.get(value, 'table-light')