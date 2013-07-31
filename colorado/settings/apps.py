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
    'django.contrib.admin',
    'django.contrib.admindocs',

    # 3rd party
    'coffin',
    'debug_toolbar',
    'djgeojson',
    'pipeline',
    'south',

    # core
    'colorado.apps.gundeaths',
    'colorado.apps.news',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# templates
JINJA2_EXTENSIONS = (
    'pipeline.jinja2.ext.PipelineExtension',
)

# staticfiles
# asset config is in assets.py
STATICFILES_STORAGE = "pipeline.storage.PipelineCachedStorage"

WORDPRESS_BLOG_URL = "http://coloradogundeaths.com"


