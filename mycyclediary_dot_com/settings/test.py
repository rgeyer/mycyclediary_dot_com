DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/code/mycyclediary_dot_com_sqlite3-test',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    },
    # 'mongo': {
    #     'ENGINE': 'django_mongodb_engine',
    #     'NAME': 'mycycledairy_dot_com_mongodb',
    #     'HOST': os.environ['CYCLEDIARYMONGO1_PORT_27017_TCP_ADDR'],
    #     'PORT': os.environ['CYCLEDIARYMONGO1_PORT_27017_TCP_PORT'],
    #     'USER': '',
    #     'PASSWORD': '',
    # },
}
