import csv
import logging
import urllib2

import pytz

from dateutil.parser import parse
from django.conf import settings
from django.template.defaultfilters import slugify

from .models import Method, Race, Incident, Victim

log = logging.getLogger('colorado.apps.gundeaths')

def load_victims(file, public=False):
    """
    Load Victim records from an open CSV file. 
    Expects the following case-sensitive fields:

    Name
        Full name of victim. Not always published.
    
    Published Name (optional)
        Alternate name for publishing. Useful for "unnamed" victims.
    
    Incident date
        When the incident occurred, which may not be the date of death.
    
    Date of death (optional)
        Date of death, if different from incident date.
    
    Type
        Can be: homicide, suicide, accidental death, officer-involved
    
    Age (optional)
        An integer.
    
    Race (optional)
        White, Black, etc. This is as police or coroners describe it,
        which may be different from the Census definition.
    
    Gender (optional)
        Male or Female.
    
    DOB (optional)
        A date. Will be passed to dateutil.parser.parse
    
    Address (optional)
        Address for the incident. Will be geocoded with City and CO.
    
    City (optional)
        City for the incident. Will be geocoded with Address.
    
    County (optional)
        Not used yet. We'll use this when geocoding fails.
    
    Home Address (optional)
        Private. Used for our own reporting.
    
    Home City (optional)
        Private. Used for our own reporting.

    Type of gun (optional)
        Not used yet.
    
    Veteran (optional)
        Not used yet.
        
    Obituary (optional)
        Link to official obit.

    """
    # normalize genders
    GENDERS = {
        'm'     : 'male',
        'male'  : 'male',
        'man'   : 'male',
        'f'     : 'female',
        'female': 'female',
        'woman' : 'female'
    }

    reader = csv.DictReader(file)
    for row in reader:

        # get categorical objects first
        race, created = get_or_create_cat(Race, row['Race'])

        method, created = get_or_create_cat(Method, row['Type'])

        gender = row['Gender'].strip().lower()
        gender = GENDERS.get(gender)

        residence_address = ", ".join((row['Home Address'], row['Home City']))

        incident, created = Incident.objects.get_or_create(
            datetime=safe_date(row['Incident date']),
            address=row['Address'],
            city=row['City'],
            defaults={
                'public': public
            }
        )

        log_created(incident, created)

        victim, created = Victim.objects.get_or_create(
            name=row['Name'].strip(),
            incident=incident,
            defaults={
                'gender': gender,
                'race'  : race,
                'method': method,
                'age'   : safe_type(int, row['Age']),
                'dob'   : safe_date(row['DOB']),
                'dod'   : safe_date(row['Date of death']),
                'residence_address': residence_address,
                'obit'  : row['Obituary'],
                'public': public
            })

        log_created(victim, created)


def get_or_create_cat(Model, name, **defaults):
    """
    Runs Thing.objects.get_or_create for CategoryBase models,
    returning obj, created.

    If name is falsy, returns None, False.
    """
    name = unicode(name).strip()
    if not name:
        return None, False

    slug = slugify(name)
    defaults['name'] = name
    obj, created = Model.objects.get_or_create(slug=slug, defaults=defaults)
    log_created(obj, created)

    return obj, created


def log_created(obj, created):
    """
    Logs object creation.
    """
    if created:
        log.debug('%s created: %s', obj.__class__.__name__, obj)


def safe_type(cast, value, default=None):
    """
    Convert value into cast type, falling back to default on ValueError
    """
    try:
        return cast(value)
    except ValueError:
        return default

def safe_date(date_str, default=None):
    """
    Safely returns a timezone-aware datetime object, or default.
    """
    if not unicode(date_str).strip():
        return default

    tz = pytz.timezone(settings.TIME_ZONE)

    try:
        return parse(date_str).replace(tzinfo=tz)
    except (AttributeError, ValueError):
        return default

