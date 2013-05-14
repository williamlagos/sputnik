import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('William Oliveira de Lagos', 'william@efforia.com.br'),
)
MANAGERS = ADMINS

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'd6i6a0klirtqjd',
    'HOST': 'ec2-54-243-243-176.compute-1.amazonaws.com',
    'PORT': 5432,
    'USER': 'kkoaphemdgvutt',
    'PASSWORD': 'ztTIw8EcIYX2UlNolrVmTb8yZQ'
  }
}

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = os.path.abspath('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.abspath('core/public'),
    os.path.abspath('spread/public'),
    os.path.abspath('promote/public'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'x5dvfbk$u-(07^f1229p*_%rcuc+nka45j6awo==*jkyjiucql'

TEMPLATE_LOADERS = (
    ('jade.ext.django.Loader',(
    	'django.template.loaders.filesystem.Loader',
    	'django.template.loaders.app_directories.Loader',
    )),
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'efforia.urls'
WSGI_APPLICATION = 'efforia.wsgi.application'
TEMPLATE_DIRS = (
    os.path.abspath('static'),
)

EFFORIA_APPS = ('spread','promote')
EFFORIA_OBJS = {
    'spread':  ['Playable','Spreadable','Image','Product'],
    'promote': ['Project','Event']
}
EFFORIA_NAMES = {
    'spread': ('Espalhe','spreads'),
    'promote': ('Promova','create')
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap','gunicorn','south',
    'django.contrib.admin',
    'paypal','pagseguro',
    'core','infinite'
]

INSTALLED_APPS.extend(EFFORIA_APPS)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'core.Profile'

PAYPAL_RECEIVER_EMAIL = 'caokzu@gmail.com'
PAYPAL_NOTIFY_URL = 'http://www.efforia.com.br/paypal'
PAYPAL_RETURN_URL = 'http://www.efforia.com.br/'
PAYPAL_CANCEL_RETURN = 'http://www.efforia.com.br/cancel'

PAGSEGURO_EMAIL_COBRANCA = 'contato@efforia.com.br' 
PAGSEGURO_TOKEN = '1a3ea7wq2e7eq8e1e223add23ad23'
PAGSEGURO_URL_RETORNO = '/pagseguro/retorno/'
PAGSEGURO_URL_FINAL = '/obrigado/' 
PAGSEGURO_ERRO_LOG  = '/tmp/pagseguro_erro.log'
