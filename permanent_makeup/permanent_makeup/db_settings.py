import os
from pathlib import Path
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

CLOUD_DB = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'URL': env('DATABASE_URL'),
        'NAME': env('PGDATABASE'),
        'USER': env('PGUSER'),
        'PASSWORD': env('PGPASSWORD'),
        'HOST': env('PGHOST'),
        'PORT': env("PGPORT"),
    }
}

LOCAL_DB = {
        'default' : {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

