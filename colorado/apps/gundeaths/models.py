import datetime

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.db.models import signals
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

from django_localflavor_us.models import USStateField

from model_utils import Choices
from model_utils.models import TimeStampedModel
from nameparser import HumanName

from .managers import PersonManager

from geopy import geocoders

g = geocoders.GoogleV3()

DEFAULT_STATE = getattr(settings, 'HW_DEFAULT_STATE', 'CO')
DEFAULT_EMBED_HEIGHT = getattr(settings, 'HW_DEFAULT_EMBED_HEIGHT', 350)

# all our base models are belonging to here

class CategoryBase(TimeStampedModel):
    """
    Base class for anything that looks and acts like a taxonomy.
    These all have the following fields:
     - name
     - slug
     - description (optional)
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.slugify()
        super(CategoryBase, self).save(*args, **kwargs)

    def slugify(self):
        return slugify(self.name)


class Person(TimeStampedModel):
    """
    A base class for people
    """
    # static properties
    GENDERS = Choices(
        ('female', 'Female'),
        ('male', 'Male'),
    )

    NAME_FIELDS = ('first', 'middle', 'last', 'suffix')

    public = models.BooleanField(default=False)

    # name
    first = models.CharField('First name', max_length=100)
    middle = models.CharField('Middle name', max_length=100, blank=True)
    last = models.CharField('Last name', max_length=100)
    suffix = models.CharField('Suffix', max_length=10, blank=True)

    slug = models.SlugField(unique=True)

    # metadata
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, choices=GENDERS)

    bio = models.TextField(blank=True)

    objects = PersonManager()

    class Meta:
        abstract = True
        ordering = ('last', 'first')

    def __unicode__(self):
        return self.name

    # name parsing
    def _get_name(self):
        "Join name parts into one string"
        parts = [getattr(self, f) for f in self.NAME_FIELDS]
        parts = filter(bool, parts)
        return u" ".join(parts)

    def _set_name(self, name):
        "Parse name parts from a name string"
        name = HumanName(name)
        self.first = name.first
        self.middle = name.middle
        self.last = name.last
        self.suffix = name.suffix

    name = property(_get_name, _set_name)

    def save(self, *args, **kwargs):
        self._clean_name_fields()
        if not self.slug:
            self.slug = self.slugify()
        super(Person, self).save(*args, **kwargs)

    def _clean_name_fields(self):
        "Strip whitespace from name fields"
        for part in self.NAME_FIELDS:
            field = getattr(self, part)
            setattr(self, part, field.strip())

    def slugify(self, n=0):
        slug = slugify(self.name)
        if n:
            slug = "%s-%i" % (slug, n)
        try:
            self.__class__.objects.get(slug__iexact=slug)
            return self.slugify(n + 1)
        except self.__class__.DoesNotExist:
            return slug

##################
# Concrete models 
##################

class Incident(TimeStampedModel):
    """
    A single incident, with one or more victims.
    People will be attached to this model.
    """
    # TODO Date/Time fields

    address = models.CharField("Street Address", max_length=255)
    city = models.CharField(max_length=255)
    state = USStateField(default=DEFAULT_STATE)
    point = models.PointField(blank=True, null=True)

    # TODO boundaries

    @property
    def location(self):
        if self.address:
            return "%s, %s, %s" % (self.address, self.city, self.state)

    def geocode(self, reset=False):
        if not self.location:
            return
        
        if not self.point or reset:
            try:
                place, (lat, lng) = list(g.geocode(self.location, exactly_one=False))[0]
                return Point(lng, lat)
            except Exception, e: # no results, should log this
                pass
        else:
            return self.point





