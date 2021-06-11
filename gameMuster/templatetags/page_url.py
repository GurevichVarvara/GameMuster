"""Generating page url templatetag"""
import string
from django import template

register = template.Library()


@register.filter(name="get_page_url")
def get_page_url(full_path, num_of_page):
    """Generate page url by current full url path"""
    num_of_page = str(num_of_page)

    if "?" in full_path and "page" in full_path:
        new_path = full_path.rstrip(string.digits) + num_of_page
    elif "?" in full_path:
        new_path = full_path + "&page=" + num_of_page
    else:
        new_path = full_path + "?page=" + num_of_page

    return new_path
