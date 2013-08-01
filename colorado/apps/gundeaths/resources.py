"""
API resources for gundeaths models.
"""
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS

from .models import Method, Race, Incident, Victim


class MethodResource(ModelResource):

	class Meta:
		allowed_methods = ('get',)
		queryset = Method.objects.all()
		filtering = {'name': ALL, 'slug': ALL}


class RaceResource(ModelResource):

	class Meta:
		allowed_methods = ('get',)
		queryset = Race.objects.all()
		filtering = {'name': ALL, 'slug': ALL}


class IncidentResource(ModelResource):

	location = fields.CharField(attribute='location', blank=True, null=True)

	victims = fields.ToManyField('colorado.apps.gundeaths.resources.VictimResource',
		'victims', blank=True, null=True, full=True)

	class Meta:
		allowed_methods = ('get',)
		queryset = (Incident.objects.public()
					.filter(point__isnull=False)
					.prefetch_related('victims'))

		excludes = ('public',)
		filtering = {
			'address': ALL,
			'city': ALL,
		    'datetime': ALL,
		    'point': ALL,
		    'victims': ALL_WITH_RELATIONS
		}

		include_absolute_url = True


class VictimResource(ModelResource):

	# foreign keys
	incident = fields.ForeignKey(IncidentResource, 'incident')
	incident_id = fields.IntegerField(attribute='incident_id')

	method = fields.ForeignKey(MethodResource, 'method', blank=True, null=True, full=True)
	race = fields.ForeignKey(RaceResource, 'race', blank=True, null=True, full=True)

	# normalize names
	name = fields.CharField(attribute='get_display_name', blank=True, null=True)

	class Meta:
		allowed_methods = ('get',)
		queryset = (Victim.objects.public()
					.select_related('incident', 'race', 'method')
					.filter(incident__point__isnull=False))

		excludes = Victim.NAME_FIELDS + ('display_name', 'public', 'residence_address')

		filtering = {
			'age': ALL,
			'incident': ALL_WITH_RELATIONS,
			'name': ALL,
			'race': ALL_WITH_RELATIONS
		}
