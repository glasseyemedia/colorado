from colorado.settings import *

DEBUG = True

# heroku specific settings
GEOS_LIBRARY_PATH = '/app/.geodjango/geos/lib/libgeos_c.so'
GDAL_LIBRARY_PATH = '/app/.geodjango/gdal/lib/libgdal.so'

# s3 and static files
DEFAULT_FILE_STORAGE = STATICFILES_STORAGE = "storages.backends.s3boto.S3BotoStorage"
STATIC_URL = "http://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME