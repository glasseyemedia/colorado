from getenv import env

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # admin
    'suit',
    'suit_redactor',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # 3rd party
    'coffin',
    'debug_toolbar',
    'djgeojson',
    'flatblocks',
    'leaflet',
    'pipeline',
    'south',
    'tastypie',

    # core
    'colorado.apps.gundeaths',
    'colorado.apps.news',
)

# aws
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False


# api
API_LIMIT_PER_PAGE = 0
TASTYPIE_FULL_DEBUG = True

# debug toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# templates
JINJA2_EXTENSIONS = (
    'jinja2.ext.autoescape',
    'pipeline.jinja2.ext.PipelineExtension',
)

# maps
MAPBOX_MAP_ID = "chrisamico.map-10h9gysj"

# staticfiles
# asset config is in assets.py
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_TEMPLATE_FUNC = "_.template"

STATICFILES_STORAGE = "pipeline.storage.PipelineCachedStorage"

# flatblocks
FLATBLOCKS_AUTOCREATE_STATIC_BLOCKS = True

# django-leaflet
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (6.0, 45.0),
    'DEFAULT_ZOOM': 16,
    'TILES': 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'PLUGINS': {
        'forms': {
            'auto-include': True
        }
    }
}

# suit
SUIT_CONFIG = {
    'CONFIRM_UNSAVED_CHANGES': False
}

# wordpress
WORDPRESS_BLOG_URL = "http://coloradogundeaths.com"


