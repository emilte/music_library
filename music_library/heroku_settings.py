import django_heroku
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ALLOWED_HOSTS = ['swingkurs.herokuapp.com']

DEBUG = True

# For whitenoise, heroku
# Extra lookup directories for collectstatic to find static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Values are set in heroku dashboard
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI')
SPOTIFY_SCOPE = os.environ.get('SPOTIFY_SCOPE')
SPOTIFY_CACHE_PATH = os.path.join(BASE_DIR, os.environ.get('SPOTIFY_CACHE_PATH'))
SECRET_KEY = os.environ.get('SECRET_KEY')
SITE_ID = os.environ.get('SITE_ID')


#  Add configuration for static files storage using whitenoise, heroku
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware', # User agent
    'whitenoise.middleware.WhiteNoiseMiddleware', # whitenoise, heroku
]

MIDDLEWARE_CLASSES = [
    'whitenoise.middleware.WhiteNoiseMiddleware', # whitenoise, heroku
]

# Activate Django-Heroku.
django_heroku.settings(locals())
