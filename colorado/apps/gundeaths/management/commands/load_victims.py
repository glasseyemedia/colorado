import os
import textwrap
import urllib2

from optparse import make_option
from django.core.management.base import LabelCommand

from colorado.apps.gundeaths.models import Method, Race, Incident, Victim
from colorado.apps.gundeaths.utils import load_victims

class Command(LabelCommand):

    option_list = LabelCommand.option_list + (
        make_option('-p', '--public', dest='public', action='store_true',
            default=False, help="Make incidents and victims public"),
    )

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

    @property
    def help(self):
        return textwrap.dedent(self.handle_label.__doc__).strip()