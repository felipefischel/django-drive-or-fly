import io
import os
from urllib.parse import urlparse

import environ

# Import the original settings from each template
from .basesettings import *

# Load the settings from the environment variable
env = environ.Env()
env.read_env(io.StringIO(os.environ.get("APPLICATION_SETTINGS", None)))

# Setting this value from django-environ
SECRET_KEY = env("SECRET_KEY")

# If defined, add service URL to Django security settings
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc,"127.0.0.1"]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
else:
    ALLOWED_HOSTS = ["*"]

# Default false. True allows default landing pages to be visible
DEBUG = env("DEBUG", default=False)


# Set this value from django-environ
DATABASES = {"default": env.db()}

# Change database settings if using the Cloud SQL Auth Proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 3306

if "myproject" not in INSTALLED_APPS:
     INSTALLED_APPS += ["myproject"] # for custom data migration

# Define static storage via django-storages[google]
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
STATICFILES_DIRS = [
    'TransportationComparison/static/',
]
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"


DATE_INPUT_FORMATS = ['%Y-%m-%d']

GOOGLE_MAPS_API_KEY=env("GOOGLE_MAPS_API_KEY")
COLLECT_API_KEY=env("COLLECT_API_KEY")
AMADEUS_API_KEY=env("AMADEUS_API_KEY")
AMADEUS_API_SECRET=env("AMADEUS_API_SECRET")


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
