"""
News views:
 - blog index
 - individual posts
 - category views
"""
from coffin.shortcuts import render
from django.conf import settings

from .wordpress import WordPress

PER_PAGE = getattr(settings, 'WORDPRESS_POSTS_PER_PAGE', 10)

wp = WordPress(settings.WORDPRESS_SITE_SLUG)

def blog_index(request, page=1):
	"""
	Get latest posts, or a page or posts.
	"""
	posts = wp.posts(page=page, number=PER_PAGE)
	return render(request, 'news/blog_index.html', posts)