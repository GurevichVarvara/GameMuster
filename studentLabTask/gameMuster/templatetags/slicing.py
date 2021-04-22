from django import template

register = template.Library()


@register.filter(name='cut_last_char')
def cut_last_char(value):
    return value[:-1]
