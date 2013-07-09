"""
WordPress utils.
"""
import urlparse
import requests

class WordPress(object):
	"""
	A little wordpress client built around the Jetpack API.
	"""
	def __init__(self, slug):
		self.slug = slug
		self.url = "https://public-api.wordpress.com/rest/v1/sites/%s/" % slug

	def posts(self, **filters):
		url = urlparse.urljoin(self.url, 'posts')
		r = requests.get(url, params=filters)
		return r.json()