"""
Custom filters and objects for news-related templates.
"""
from coffin import template
from django.utils.dateformat import DateFormat

register = template.Library()

from dateutil.parser import parse

@register.filter
def parsedate(value, format=None):
    dt = parse(value)
    if format:
        return DateFormat(dt).format(format)
    return dt