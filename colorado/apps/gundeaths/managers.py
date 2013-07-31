from itertools import groupby
from django.contrib.gis.db.models.query import GeoQuerySet
from model_utils.managers import PassThroughManager
from nameparser import HumanName

class PersonQuerySet(GeoQuerySet):

    def public(self):
        return self.filter(public=True)

    def filter(self, *args, **kwargs):
        """
        Override default filter method to parse out `name` argument
        into consituent fields. Also works for `get` and `get_or_create`.
        """
        from .models import Person
        if "name" in kwargs:
            name = kwargs.pop('name')
            name = HumanName(name)
            for field in Person.NAME_FIELDS:
                kwargs[field] = getattr(name, field)

        return super(PersonQuerySet, self).filter(*args, **kwargs)


class VictimQuerySet(PersonQuerySet):

    def by_incident_date(self, format=None):
        """
        Group by incident date. 
        Pass in a format to create larger groups (months, for example).
        """
        if format:
            return groupby(self, lambda v: v.incident.datetime.strftime(format))
        else:
            return groupby(self, lambda v: v.incident.datetime)

    def by_incident(self):
        """
        Group by incident ID.
        """
        return groupby(self, lambda v: v.incident_id)


class IncidentQuerySet(GeoQuerySet):
    """
    A queryset for incidents, which needs spatial stuff and publicness
    """
    def public(self):
        return self.filter(public=True)


PersonManager = PassThroughManager.for_queryset_class(PersonQuerySet)
VictimManager = PassThroughManager.for_queryset_class(VictimQuerySet)
IncidentManager = PassThroughManager.for_queryset_class(IncidentQuerySet)
