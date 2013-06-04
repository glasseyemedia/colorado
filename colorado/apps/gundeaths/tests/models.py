from django.test import TestCase
from django.utils import timezone

from colorado.apps.gundeaths.models import Incident, Victim

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


