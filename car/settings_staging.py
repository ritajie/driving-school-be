from .settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "car",
        "USER": "root",
        "PASSWORD": "123",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    },
}
