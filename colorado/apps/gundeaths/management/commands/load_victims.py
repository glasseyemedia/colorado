import os
import urllib2
from django.core.management.base import LabelCommand

from colorado.apps.gundeaths.models import Method, Race, Incident, Victim
from colorado.apps.gundeaths.utils import load_victims

class Command(LabelCommand):

    def handle_label(self, label, **options):
        """
        Load victims and incidents from a file or URL.
        This will throw an error if neither file nor URL exist.
        """

        if os.path.isfile(label):
            with open(label) as f:
                load_victims(f)
        else:
            f = urllib2.urlopen(label)
            load_victims(f)

        self.stdout.write('Total incidents: %i' % Incident.objects.count())
        self.stdout.write('Total victims: %i' % Victim.objects.count())