import csv
import logging
import urllib2
import urlparse
import pytz

from dateutil.parser import parse
from django.conf import settings
from django.template.defaultfilters import slugify
from wordpress import WordPress, WordPressError

from .models import Method, Race, Incident, Victim

log = logging.getLogger('colorado.apps.gundeaths')

# create a wordpress object, sans cache
wp = WordPress(settings.WORDPRESS_BLOG_URL, None)


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

    WP_URL
        Link to a blog post that can be imported as incident.description

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

        WP_URL = row.get('WP_URL', '').strip()
        if not WP_URL:
            log.debug('No blog post associated with victim: %s', victim.name)
            continue

        # fetch post JSON
        path = urlparse.urlparse(WP_URL).path
        post = wp.proxy(path)

        # set incident description from post
        incident.desciption = post['post']['content']
        incident.save()

        log.debug('Set description for incident: %s', unicode(victim.incident).encode('utf-8'))


def load_summaries(file):
    """
    Load summaries from WordPress, using an open CSV file.
    This function expects a column called WP_URL, pointing to a single blog post.
    The blog must have the WordPress JSON API plugin installed and configured to allow
    proxying (by appending `json=1` to the querystring).

    This also assumes victims and incidents have already been loaded into the database.
    It will check for existence but skip names that don't match an existing record.
    """
    reader = csv.DictReader(file)

    for row in reader:

        # get victim by name
        name = row.get('Name').strip()
        try:
            victim = Victim.objects.get(name=name)
        
        # catch unmatched names, probably not yet loaded
        except Victim.DoesNotExist:
            log.debug('Victim not found: %s', name)
            continue

        # catch multiples, probably "unnamed man"
        except Victim.MultipleObjectsReturned:
            log.debug('Multiple victims found: %s', name)
            continue

        WP_URL = row.get('WP_URL').strip()
        if not WP_URL:
            log.debug('No blog post associated with victim: %s', name)
            continue

        # fetch post JSON
        path = urlparse.urlparse(WP_URL).path
        post = wp.proxy(path)

        # set incident description from post
        victim.incident.desciption = post['post']['content']
        victim.incident.save()

        log.debug('Set description for incident: %s', unicode(victim.incident).encode('utf-8'))


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

