DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'd8lj2qraq5jbrt',
    'HOST': 'ec2-23-23-234-207.compute-1.amazonaws.com',
    'PORT': 5432,
    'USER': 'edjzbpcwxlmfyv',
    'PASSWORD': 'vhm_pQhDcjoux0iELZDH4p5-cn'
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
DEBUG = 'TRUE'
