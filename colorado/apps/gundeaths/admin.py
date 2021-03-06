import csv
import datetime

from django.contrib.gis import admin
from django.db.models import Count
from django.http import HttpResponse
from django.forms import ModelForm, TextInput

#from suit.widgets import SuitSplitDateTimeWidget
from redactor.widgets import AdminRedactorEditor

from .models import Method, Race, Incident, Victim
from .models import DATE_FORMAT, DATETIME_FORMAT

####################
# Forms
####################

class IncidentForm(ModelForm):
    """
    Override the default Incident form to customize widgets
    """
    class Meta:
        model = Incident
        widgets = {
            #'datetime': SuitSplitDateTimeWidget,
            'description': AdminRedactorEditor(),
        }


class PersonForm(ModelForm):
    """
    Override the default Person form
    """
    class Meta:
        model = Victim
        widgets = {
            'bio': AdminRedactorEditor(),
            'residence_address': TextInput
        }

############
# Actions
############

def make_public(modeladmin, request, queryset):
    queryset.update(public=True)
make_public.short_description = "Mark selected items as public"

##############
# ModelAdmins
##############

class VictimInline(admin.StackedInline):
    # classes = ('collapse open',)
    extra = 1
    form = PersonForm
    prepopulated_fields = {'slug': Victim.NAME_FIELDS }
    model = Victim


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
    actions = [make_public, 'export']
    form = IncidentForm
    inlines = [VictimInline]
    
    date_hierarchy = "datetime"
    list_display = ('datetime', 'address', 'city', 'victim_links', 'public')
    list_filter = ('public', 'city')

    fieldsets = (
        (None, {
            'fields': ('public', 'datetime', 'address', 'city', 'state', 'point')
        }),

        (None, {
            'fields': ('description',),
            #'classes': ('full-width',)
        }),
    )

    def victim_links(self, obj):
        return ", ".join(unicode(v) for v in obj.victims.all())

    def export(self, request, queryset):
        """
        Export victims from these incidents.
        """
        qs = Victim.objects.filter(incident__in=queryset).select_related('incident')
        return export_victims(qs)


class VictimAdmin(admin.ModelAdmin):
    actions = [make_public, 'export']
    form = PersonForm

    exclude = ('slug',)

    list_display = ('name', 'method', 'dod', 'dob', 'age', 'gender', 'race', 'public')
    list_editable = ('gender', 'race')
    list_filter = ('public', 'method', 'age', 'race', 'gender')

    search_fields = Victim.NAME_FIELDS

    def queryset(self, request):
        """
        Make sure we select_related.
        """
        qs = super(VictimAdmin, self).queryset(request)
        qs = qs.select_related('incident', 'method', 'race')
        return qs

    def save_model(self, request, obj, form, change):
        """
        Save hook to auto-fill slug.
        """
        obj.slug = obj.slugify()
        obj.save()

    def export(self, request, queryset):
        """
        Dump victims to CSV.
        """
        return export_victims(queryset)


def export_victims(queryset):
    """
    Dump victims to CSV. 
    Takes a victims queryset and returns a CSV response.
    """
    # get a response we can write to
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = "attachment; filename=victims.csv"

    # get a writer
    incident_fields = ['datetime', 'address', 'city', 'state', 'county']
    victim_fields = [
        'id', 'first', 'middle', 'last', 'suffix', 'display_name', 'alias',
        'dob', 'dod', 'age', 'gender', 'method', 'race', 'place_of_death']

    fields = incident_fields + victim_fields

    writer = csv.DictWriter(response, fields)

    # write header
    writer.writeheader()

    # prefetch and select related
    queryset = queryset.select_related('incident', 'race', 'method')

    for victim in queryset:
        row = {}
        for f in fields:
            if hasattr(victim, f):
                row[f] = unicode(getattr(victim, f, '')).encode('utf-8')
            else:
                row[f] = unicode(getattr(victim.incident, f, '')).encode('utf-8')

            # counties are special
            if victim.incident:
                row['county'] = victim.incident.get_county()
            else:
                row['county'] = None

        writer.writerow(row)

    return response


admin.site.register(Method, SimpleAdmin)
admin.site.register(Race, SimpleAdmin)
admin.site.register(Incident, IncidentAdmin)
admin.site.register(Victim, VictimAdmin)