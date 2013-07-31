from django.conf.urls import patterns, url

from .views import wp_proxy

urlpatterns = patterns('',

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[-\w]+)/$',
    	wp_proxy,
    	{'single': True, 'template': 'news/blogpost_detail.html'},
    	name='blog_post_detail'),

    url(r'^page/(?P<page>\d+)/$',
    	wp_proxy,
    	name='blog_index_page'),

    # a page, proxied from wordpress
    # here for url convenience
    url(r'^(?P<slug>[-\w]+)/$',
    	wp_proxy,
    	{'single': True, 'template': 'news/page.html'},
    	name='blog_page'),

    # catch anything else that falls through
    url(r'^', wp_proxy, name='blog_index'),

)