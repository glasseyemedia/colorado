# app-related settings, including middleware

import dj_redis_url
from getenv import env

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
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
    'redactor',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # 3rd party
    'tastypie',
    'boundaryservice',
    'coffin',
    'debug_toolbar',
    'disqus',
    'djgeojson',
    'flatblocks',
    'leaflet',
    'pipeline',
    'south',

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

# caching and redis
REDIS = dj_redis_url.config(default='redis://localhost:6379')

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%(HOST)s:%(PORT)s' % REDIS,
        'OPTIONS': {
            'DB': REDIS['DB'],
            'PASSWORD': REDIS['PASSWORD'],
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

CACHE_MIDDLEWARE_SECONDS = 0
CACHE_MIDDLEWARE_KEY_PREFIX = "coguns"
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = False

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

# disqus
DISQUS_API_KEY = "KZizNwNvU3pGYiZonR3TiRXg5f51DWauO821oGF8zXCU9OK4nP1oCGu0kZnkZ7Ho"
DISQUS_WEBSITE_SHORTNAME = "coloradogundeaths"

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
WORDPRESS_BLOG_URL = "http://wordpress.coloradogundialog.com"


