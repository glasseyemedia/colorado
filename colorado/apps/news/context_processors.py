"""
Context processors related to news.
"""
from django.conf import settings

def news_settings(request):
	"""
	Inject useful settings into every context.
	"""
	return {
	    'WORDPRESS_BLOG_URL': settings.WORDPRESS_BLOG_URL
	}
