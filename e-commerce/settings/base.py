from __future__ import absolute_import, unicode_literals
import os


from decouple import config

# export DJANGO_SETTINGS_MODULE=e-commerce.settings.development

os.environ.setdefault('DJANGO_SETTING_MODULU','e-commerce.settings.development')

SECRET_KEY = 'jx@fm!+yqselbaqp^z&hnckmj$d*!lxmtl-rlsezy-(-bct=k%'

# CELERY STUFF
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER='bappi.ajmalaamir@gmail.com'
EMAIL_HOST_PASSWORD='b01710729756'
EMAIL_PORT = 587
EMAIL_USE_TLS=True


EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For RabbitMQ
BROKER_URL = 'amqp://127.0.0.1/5672/'
CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
# Celery Data Format
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dhaka'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!







# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    'crispy_forms',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'core', # for custom  commands and more



    'djcelery',
    'djcelery_email',
]

MIDDLEWARE = [
     'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','dj-ecom.herokuapp.com']





ROOT_URLCONF = 'e-commerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

WSGI_APPLICATION = 'e-commerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators




# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_venv')]
# VENV_PATH = os.path.dirname(BASE_DIR)

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
PROJECT_ROOT   =   os.path.join(os.path.abspath(__file__))
MEDIA_URL = '/media/'

# AUTHENTICATION



AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_EMAIL_VERIFICATION = 'none'



SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# heroku setup
#  Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# heroku setup
import dj_database_url
prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)