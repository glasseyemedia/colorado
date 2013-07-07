from django.conf.urls import patterns, url, include

from .views import VictimList

urlpatterns = patterns('',
    url(r'^$', VictimList.as_view(), name='gundeaths_victim_list'),
)