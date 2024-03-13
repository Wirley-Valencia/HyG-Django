import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SQLITE = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
#     }
# }

MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hygdb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3307'
    }
}
# MYSQL = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'hygdb',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '3306'
#     }
# }


# POSTGRESQL = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'db',
#         'USER': 'postgres',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '5432'
#     }
# }
