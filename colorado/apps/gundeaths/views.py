"""
Views for victims:
 - a list for a sortable table
 - a list for a memorial wall
 - a list view, for a map?
 - an incident detail, with profiles
"""

from django.views.generic import ListView
from coffin.shortcuts import render
from .models import Victim


class VictimList(ListView):
    """
    A generic list of victims.
    Using a class-based view here so it's easier to
    reuse with different templates.
    """
    queryset = Victim.objects.public()

    def render_to_response(self, context, **response_kwargs):
        """
        Overriding to use jinja2 templates
        """
        templates = self.get_template_names()
        return render(self.request, templates, context, **response_kwargs)

