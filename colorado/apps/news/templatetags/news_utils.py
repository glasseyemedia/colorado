"""
Custom filters and objects for news-related templates.
"""
from coffin import template
from django.utils.dateformat import DateFormat

from colorado.apps.news.views import wp

register = template.Library()

from dateutil.parser import parse

@register.filter
def parsedate(value, format=None):
    dt = parse(value)
    if format:
        return DateFormat(dt).format(format)
    return dt


@register.object
def wp_pages():
	"""
	Return a list of WordPress-created pages.
	Includes only title and slug to save bandwidth.
	"""
	resp = wp.get_page_index(include='title,slug')
	return resp.get('pages', [])