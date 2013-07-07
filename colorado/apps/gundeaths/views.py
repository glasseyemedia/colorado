"""
Views for victims:
 - a list for a sortable table
 - a list for a memorial wall
 - a list view, for a map?
 - an incident detail, with profiles
"""

from django.views.generic import ListView

from .models import Victim


class VictimList(ListView):
    """
    A generic list of victims.
    Using a class-based view here so it's easier to
    reuse with different templates.
    """
    queryset = Victim.objects.public()