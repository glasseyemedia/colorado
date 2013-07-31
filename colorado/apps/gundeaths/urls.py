from django.conf.urls import patterns, url, include

from .views import IncidentDetail, VictimList

urlpatterns = patterns('',
    url(r'^victims/$', 
        VictimList.as_view(), 
        name='gundeaths_victim_list'),

    url(r'^incidents/(?P<pk>\d+)/$', 
        IncidentDetail.as_view(), 
        name='gundeaths_incident_detail'),
)