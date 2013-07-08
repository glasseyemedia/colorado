"""
Views for victims:
 - a list for a sortable table
 - a list for a memorial wall
 - a list view, for a map?
 - an incident detail, with profiles
"""

from django.views.generic import DetailView, ListView
from coffin.shortcuts import render
from .models import Incident, Victim

class JinjaMixin(object):

    def render_to_response(self, context, **response_kwargs):
        """
        Overriding to use jinja2 templates
        """
        templates = self.get_template_names()
        return render(self.request, templates, context, **response_kwargs)


class VictimList(JinjaMixin, ListView):
    """
    A generic list of victims.
    Using a class-based view here so it's easier to
    reuse with different templates.
    """
    queryset = Victim.objects.public().select_related('incident')


class IncidentDetail(JinjaMixin, DetailView):
    """
    Detail view for a single incident, which may have multiple victims.
    """
    queryset = Incident.objects.public().prefetch_related('victims')