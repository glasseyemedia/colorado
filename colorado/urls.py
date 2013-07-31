from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'colorado.views.home', name='home'),
    # url(r'^colorado/', include('colorado.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # core
    url(r'^', include('colorado.apps.gundeaths.urls')),

    url(r'^', include('colorado.apps.news.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns() #only when settings.DEBUG == True

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^500/$', TemplateView.as_view(template_name='500.html')),
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    )
