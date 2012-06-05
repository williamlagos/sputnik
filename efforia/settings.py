DATABASE_ENGINE='django.db.backends.postgresql_psycopg2'
DATABASE_NAME='efforia'
ROOT_URLCONF='urls'
INSTALLED_APPS=('core','play','spread','explore','south','create',
				'paypal.standard.ipn',
				'django.contrib.contenttypes',
                'django.contrib.auth',
                'django.contrib.sessions')

#PAYPAL_RECEIVER_EMAIL = "caokzu_1338898743_biz@live.com"
PAYPAL_RECEIVER_EMAIL = "caokzu@gmail.com"
