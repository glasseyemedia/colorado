"""
Views for victims:
 - a list for a sortable table
 - a list for a memorial wall
 - a list view, for a map?
 - an incident detail, with profiles
"""
import json

from coffin.shortcuts import get_object_or_404, render
from django.db.models import Count
from django.http import HttpResponse
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


def incident_detail(request, pk):
    """
    Detail view for a single incident, which may have multiple victims.
    """
    incident = get_object_or_404(Incident.objects.public(), pk=pk)
    victims = list(incident.victims.public()
                    .select_related('incident', 'race', 'method'))

    return render(request, 'gundeaths/incident_detail.html', {
        'incident': incident, 'victims': victims
    })

#############
# Aggregates
#############

def victims_by_method(request):
    """
    Return victims by method, as JSON.
    """
    victims = Victim.objects.public()
    methods = (victims.order_by('method')
                .values('method__name')
                .annotate(count=Count('method__name')))

    data = {
        'count': victims.count(),
        'methods': [m for m in methods if m['count'] > 0]
    }

    return HttpResponse(json.dumps(data), content_type='application/json')





