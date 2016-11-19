import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(__file__)

SECRET_KEY = '6_g@d!*!u2ar=d*5vuum@s%fdtw-yz@y#1=b&b36xivry@^ijg'

DEBUG = True

ALLOWED_HOSTS = []

# Openshift identifier
ON_OPENSHIFT = False
if 'OPENSHIFT_REPO_DIR' in os.environ:
    ON_OPENSHIFT = True

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'msgapi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'myproj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, '../templates')],
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

WSGI_APPLICATION = 'myproj.wsgi.application'

# For Openshift use a DB path which is outside GIT as it will get wiped off when "git push" is done
if ON_OPENSHIFT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.getenv('OPENSHIFT_DATA_DIR'), 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

# Configure static root for collectstatic
if ON_OPENSHIFT:
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL.strip("/"))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'debug.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Celery setup
import djcelery
djcelery.setup_loader()
MAX_RETRIES = 4
if ON_OPENSHIFT:                # Celery setup on openshift
    BROKER_TRANSPORT = 'redis'
    BROKER_HOST = "127.10.78.130"
    BROKER_PORT = 16379
    # BROKER_USER = "guest"
    BROKER_PASSWORD = "ZTNiMGM0NDI5OGZjMWMxNDlhZmJmNGM4OTk2ZmI5"
    BROKER_VHOST = "0"
    CELERYD_CONCURRENCY = 3
else:                           # Celery setup on local environment
    BROKER_TRANSPORT = 'redis'
    BROKER_HOST = "localhost"
    BROKER_PORT = 6379
    # BROKER_USER = "guest"
    # BROKER_PASSWORD = "guest"
    BROKER_VHOST = "0"
    CELERYD_CONCURRENCY = 3
