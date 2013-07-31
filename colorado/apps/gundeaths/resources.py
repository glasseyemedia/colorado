"""
API resources for gundeaths models.
"""
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS

from .models import Race, Incident, Victim

class RaceResource(ModelResource):

	class Meta:
		allowed_methods = ('get',)
		queryset = Race.objects.all()
		filtering = {'name': ALL, 'slug': ALL}


class IncidentResource(ModelResource):

	location = fields.CharField(attribute='location', blank=True, null=True)

	# point = GeometryApiField(attribute='point', blank=True, null=True)

	class Meta:
		allowed_methods = ('get',)
		queryset = Incident.objects.public().filter(point__isnull=False)
		excludes = ('public',)
		filtering = {
			'address': ALL,
			'city': ALL,
		    'datetime': ALL,
		    'point': ALL
		}


class VictimResource(ModelResource):

	# foreign keys
	incident = fields.ForeignKey(IncidentResource, 'incident')
	incident_id = fields.IntegerField(attribute='incident_id')

	race = fields.ForeignKey(RaceResource, 'race', blank=True, null=True, full=True)

	# normalize names
	name = fields.CharField(attribute='get_display_name', blank=True, null=True)

	class Meta:
		allowed_methods = ('get',)
		queryset = (Victim.objects.public()
					.select_related('incident', 'race')
					.filter(incident__point__isnull=False))

		excludes = Victim.NAME_FIELDS + ('display_name', 'public', 'residence_address')

		filtering = {
			'age': ALL,
			'incident': ALL_WITH_RELATIONS,
			'name': ALL,
			'race': ALL_WITH_RELATIONS
		}
