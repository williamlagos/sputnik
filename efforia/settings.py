DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'd87i80lg975lcv',
    'HOST': 'ec2-23-23-201-251.compute-1.amazonaws.com',
    'PORT': 5432,
    'USER': 'vcrkfqjrxpdhgy',
    'PASSWORD': 'lFDRg2mdPpZvf3ya_b-cjbjx_I'
  }
}
ROOT_URLCONF='urls'
INSTALLED_APPS=('core','play','spread','create','store','explore','south',
				'paypal.standard.ipn',
				'django.contrib.contenttypes',
                'django.contrib.auth',
                'django.contrib.sessions')

PAYPAL_RECEIVER_EMAIL = "caokzu_1338898743_biz@live.com"
#PAYPAL_RECEIVER_EMAIL = "caokzu@gmail.com"
