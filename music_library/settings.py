
import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

CUSTOM_SETTINGS = ["heroku_settings", "allauth_settings"] # heroku_settings
# CUSTOM_SETTINGS = ["dev_settings", "allauth_settings", "local_settings"] # local_settings

DEBUG = False
ALLOWED_HOSTS = []

# Static
STATIC_ROOT = os.path.join(BASE_DIR, 'staticroot')
STATIC_URL = '/static/'

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, "mediaroot")
MEDIA_URL = '/media/'

# URLs
LOGIN_REDIRECT_URL = 'accounts:profile'
LOGIN_URL = 'accounts:login'
LOGOUT_REDIRECT_URL = 'accounts:login'

# Custom User model
AUTH_USER_MODEL = 'accounts.User'



# # Production settings:
SECURE_HSTS_SECONDS = 60 # TODO: Find a decent value
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# Application definition
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Imported apps
    'django_user_agents', # Recognises devices and touch capabilities
    'django_extensions', # Extended CLI commands
    'tinymce', # For HTMLField (obsolete, tinyMCE is used another way)
    'django_select2', # For improved ChoiceField widgets
    'django_seed', # Seed database easily

    # Own apps
    'accounts',
    'videos',
    'music_library',
    'info',
    'songs',
    'courses',
    'wiki',
    'events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_user_agents.middleware.UserAgentMiddleware', # User agent
]



ROOT_URLCONF = 'music_library.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'music_library.wsgi.application'

# Settings for user agent
# Cache backend is optional, but recommended to speed up user agent parsing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'nb'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Custom settings that overwrite this.
try:
    from .local_settings import *
except:
    print("== local_settings was not imported ==")

if "heroku_settings" in CUSTOM_SETTINGS:
    from .heroku_settings import *
    print("== IMPORTED: heroku_settings ==")
    # print("== heroku_settings was not imported ==")

if "dev_settings" in CUSTOM_SETTINGS:
    from .dev_settings import *
    print("== IMPORTED: dev_settings ==")
    # print("== dev_settings was not imported ==")

if "allauth_settings" in CUSTOM_SETTINGS:
    from .allauth_settings import *
    print("== IMPORTED: allauth_settings ==")




checklist = {
    'DEBUG': DEBUG,
    'SITE_ID': SITE_ID,
    # 'DATABASES': DATABASES,
    # 'SECRET_KEY': SECRET_KEY,
    # 'SPOTIFY_CLIENT_ID': SPOTIFY_CLIENT_ID,
    # 'INSTALLED_APPS': INSTALLED_APPS,
}

def check_settings(settings):
    try:
        print("|\n== CHECK SETTINGS ==")
        for k, v in settings.items():
            print("{} = {}".format(k, v))
        print('|')
    except Exception as e:
        print(e)

check_settings(checklist)
