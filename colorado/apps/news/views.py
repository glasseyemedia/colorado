"""
News views:
 - blog index
 - individual posts
 - category views
"""
from coffin.shortcuts import render
from django.conf import settings
from django.http import Http404

from wordpress import WordPress, WordPressError

wp = WordPress(settings.WORDPRESS_BLOG_URL)


def wp_proxy(request, **kwargs):
    """
    Proxy request to WordPress.
    """
    try:
        resp = wp.proxy(request.path)
    
    except WordPressError, e:
        if 'Not found' in e.args:
            raise Http404
        else:
            raise

    # get a template name, using an index by default
    template = kwargs.pop('template', 'news/blog_index.html')

    # pass any remaining kwargs into context
    resp.update(kwargs)

    # send everything along
    return render(request, template, resp)
