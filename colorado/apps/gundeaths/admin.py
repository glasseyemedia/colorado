from django.contrib.gis import admin
from django.db.models import Count

from .models import Method, Race, Incident, Victim
from .models import DATE_FORMAT, DATETIME_FORMAT

# actions
def make_public(modeladmin, request, queryset):
    queryset.update(public=True)
make_public.short_description = "Mark selected items as public"


class SimpleAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'victim_count', 'description')
    prepopulated_fields = {'slug': ('name',) }

    def queryset(self, request):
        """
        Return a queryset with victim_count attached.
        """
        qs = super(SimpleAdmin, self).queryset(request)
        qs = qs.annotate(victim_count=Count('victims'))
        return qs

    def victim_count(self, obj):
        return obj.victim_count


class IncidentAdmin(admin.OSMGeoAdmin):
    actions = [make_public]
    date_hierarchy = "datetime"
    list_display = ('datetime', 'address', 'city', 'victim_links', 'public')
    list_filter = ('public', 'city')

    def victim_links(self, obj):
        return ", ".join(unicode(v) for v in obj.victims.all())


class VictimAdmin(admin.ModelAdmin):
    actions = [make_public]

    list_display = ('name', 'method', 'dod', 'dob', 'age', 'gender', 'race', 'public')
    list_editable = ('gender', 'race')
    list_filter = ('public', 'method', 'age', 'race', 'gender')

    search_fields = Victim.NAME_FIELDS

    prepopulated_fields = {'slug': Victim.NAME_FIELDS }


admin.site.register(Method, SimpleAdmin)
admin.site.register(Race, SimpleAdmin)
admin.site.register(Incident, IncidentAdmin)
admin.site.register(Victim, VictimAdmin)