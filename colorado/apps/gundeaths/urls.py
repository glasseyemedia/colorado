from django.conf.urls import patterns, url, include

from .views import IncidentMap, VictimList, incident_detail

urlpatterns = patterns('',
    url(r'^victims/$', 
        VictimList.as_view(), 
        name='gundeaths_victim_list'),

    url(r'^incidents/$',
    	IncidentMap.as_view(),
    	name="gundeaths_incident_map"),

    url(r'^incidents/(?P<pk>\d+)/$', 
        incident_detail, 
        name='gundeaths_incident_detail'),
)