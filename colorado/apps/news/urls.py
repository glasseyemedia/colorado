from django.conf.urls import patterns, url

from .views import blog_index

urlpatterns = patterns('',
    url(r'^$', blog_index, name='blog_index'),

    url(r'^page/(?P<page>\d+)/$',
    	blog_index,
    	name='blog_index_page'),
)