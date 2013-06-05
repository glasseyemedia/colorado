import csv
import urllib2
from cStringIO import StringIO

from django.test import TestCase
from django.utils import timezone

from colorado.apps.gundeaths.models import Incident, Victim
from colorado.apps.gundeaths.utils import load_victims

class IncidentTests(TestCase):
    """
    Tests related to Incident models
    """
    def setUp(self):
        self.places = (
            ('I-25 and U.S. 50 West', 'Pueblo'),
            ('1000 block of Alcott Street', 'Denver'),
            (' 55th Street and Valmont Road', 'Boulder')
        )

    def create_incidents(self):
        for address, city in self.places:
            incident = Incident.objects.create(
                datetime=timezone.now(),
                address=address,
                city=city
            )

    def test_create_incidents(self):
        self.create_incidents()
        self.assertEqual(Incident.objects.count(), len(self.places))

    def test_geocode(self):
        self.create_incidents()

        self.assertEqual(
            Incident.objects.count(), 
            Incident.objects.filter(point__isnull=False).count()
        )


class LoadingTest(TestCase):
    """
    Tests related to data loading.
    """
    def setUp(self):
        self.url = "https://docs.google.com/spreadsheet/pub?key=0AprNP7zjIYS1dEhXRnRVTDRfRlRVcFdnVlhTcEk1N3c&single=true&gid=0&output=csv"

    def test_load_victims(self):
        """
        Ensure that load_victims gets the right number of records.
        """
        data = urllib2.urlopen(self.url).read()
        data = StringIO(data)

        reader = csv.DictReader(data)
        total = len(list(reader))

        data.seek(0)
        reader = csv.DictReader(data)

        load_victims(data)

        self.assertEqual(Victim.objects.count(), total)






