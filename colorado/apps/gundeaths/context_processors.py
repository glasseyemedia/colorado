"""
Context processors for gundeaths. Adds useful settings for maps.
"""
from django.conf import settings

def map_settings(request):
	"""
	Adds settings useful for maps.
	"""
	return {
		'MAPBOX_MAP_ID': getattr(settings, 'MAPBOX_MAP_ID', '')
	}