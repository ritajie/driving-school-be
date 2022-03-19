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

WECHAT_APP_ID = "wx8ff3e3866117040c"
WECHAT_APP_SECRET = "9f2f6f4b2d0a89ad4ae3e3cb2bcd87d8"
