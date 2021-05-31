"""Dict lookup templatetag"""
from django import template

register = template.Library()


@register.filter(name='dict_lookup')
def dict_lookup(current_dict, key):
    """Return dict value by key"""
    return current_dict[key]
