"""
Utilities and base classes for use in views across apps.
"""
from coffin.shortcuts import render

class JinjaMixin(object):

    def render_to_response(self, context, **response_kwargs):
        """
        Overriding to use jinja2 templates
        """
        templates = self.get_template_names()
        return render(self.request, templates, context, **response_kwargs)
