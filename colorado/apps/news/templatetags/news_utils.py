"""
Custom filters and objects for news-related templates.
"""
from coffin import template
from coffin.template.loader import render_to_string
from django.conf import settings
from django.utils.dateformat import DateFormat
from jinja2 import Markup
from flatblocks.models import FlatBlock

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


@register.object
def wp_sidebar(sidebar_id):
	"""
	Get a WordPress sidebar from the blog.
	"""
	return wp.method('widgets.get_sidebar', sidebar_id=sidebar_id)


@register.object
def flatblock(slug, template='flatblocks/flatblock.html'):
	"""
	Return a rendered flatblock, using template.
	"""
	AUTOCREATE = getattr(settings, 'FLATBLOCKS_AUTOCREATE_STATIC_BLOCKS', False)

	try:
		fb = FlatBlock.objects.get(slug=slug)
	except FlatBlock.DoesNotExist, e:
		if AUTOCREATE:
			fb = FlatBlock.objects.create(slug=slug)
		else:
			raise

	return Markup(render_to_string(template, {'flatblock': fb}))

