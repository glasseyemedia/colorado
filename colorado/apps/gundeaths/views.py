"""
Views for victims:
 - a list for a sortable table
 - a list for a memorial wall
 - a list view, for a map?
 - an incident detail, with profiles
"""

from django.views.generic import DetailView, ListView

from colorado.lib.views import JinjaMixin
from .models import Incident, Victim


class VictimList(JinjaMixin, ListView):
    """
    A generic list of victims.
    Using a class-based view here so it's easier to
    reuse with different templates.
    """
    queryset = (Victim.objects.public()
            .order_by('-incident__datetime')
            .select_related('incident'))


class IncidentMap(JinjaMixin, ListView):
    """
    A list of incidents, meant for mapping.
    """
    queryset = (Incident.objects.public()
            .filter(point__isnull=False))

    template_name = "gundeaths/map.html"


class IncidentDetail(JinjaMixin, DetailView):
    """
    Detail view for a single incident, which may have multiple victims.
    """
    queryset = Incident.objects.public().prefetch_related('victims')