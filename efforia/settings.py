import os



DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'd6r62o9egbu5id',
		'HOST': 'ec2-107-21-120-175.compute-1.amazonaws.com',
		'PORT': 5432,
		'USER': 'eiboktcvhbrtbs',
		'PASSWORD': 'RVpo3RO5iEKey9ndd94o_uSO-h'
	}
}



ROOT_URLCONF = 'urls'
INSTALLED_APPS = ('core','play','spread','create','store','explore','south',
		'paypal.standard.ipn',
		'django.contrib.contenttypes',
                'django.contrib.auth',
                'django.contrib.sessions',
		'django.contrib.staticfiles')
STATICFILES_DIRS = (os.path.abspath('static'),)
SECRET_KEY = ' '
PAYPAL_RECEIVER_EMAIL = 'caokzu_1338898743_biz@live.com'
#PAYPAL_RECEIVER_EMAIL = 'caokzu@gmail.com'
STATIC_URL = '/'
STATIC_ROOT = os.path.abspath('stat')
DEBUG = 'TRUE'
