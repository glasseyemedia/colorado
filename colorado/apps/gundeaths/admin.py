from django.contrib.gis import admin

from .models import Method, Race, Incident, Victim

class SimpleAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {'slug': ('name',) }


class IncidentAdmin(admin.OSMGeoAdmin):

    pass


class VictimAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': Victim.NAME_FIELDS }


admin.site.register(Method, SimpleAdmin)
admin.site.register(Race, SimpleAdmin)
admin.site.register(Incident, IncidentAdmin)
admin.site.register(Victim, VictimAdmin)