DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eep',
        'USER': 'saladrai',
        'PASSWORD': '*********',
        'HOST': '',
        'PORT': '',
    }
}

EMAIL_HOST = 'mail.itim.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = "hostmaster@itim.net"
EMAIL_HOST_PASSWORD = "******"
EMAIL_USE_TLS = True