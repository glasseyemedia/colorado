from django.conf.urls import include, url, patterns
from tastypie.api import Api

from colorado.apps.gundeaths.resources import IncidentResource, RaceResource, VictimResource

v1 = Api(api_name='v1')
v1.register(IncidentResource())
v1.register(RaceResource())
v1.register(VictimResource())

urlpatterns = patterns('',
    url(r'^', include(v1.urls)),
)