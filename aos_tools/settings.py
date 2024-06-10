"""
Django settings for aos_tools project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

import redis

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4qyvookw)ev%7yvz+og3cx)9u*a-3*mpge1%3o+2fz0%%cu3#u"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["aida.ngrok.app", "127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = ["https://aida.ngrok.app"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "data.apps.ListsConfig",
    "django_celery_results",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "aos_tools.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "aos_tools.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "aos_tools"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

BROKER_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

BCP_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Apache-HttpClient/4.5.14 (Java/17.0.9)",
    "Accept-Encoding": "br,deflate,gzip,x-gzip",
    "Client-id": os.environ.get("BCP_CLIENT_ID", ""),
    "Authorization": os.environ.get("BCP_AUTHORIZATION", ""),
    "Identity": os.environ.get("BCP_IDENTITY", ""),
}

BCP_REFRESH_TOKEN = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.VX4BV5mFgOp8nCrTPBJytRPBy12LjBjjpnVtY00bdBSUDahNlniYTKEKktsDr78NRb-8td3d0Jaw9dTqtPqFfjoDD2lBiOs6-J1JNklW3TIyPjecof43c-skqVlc5U_kf1DRH2lrCod0HvLb3EdnvAeU0fON_zYZkRcFPJ276Goyzk4dZA18yOz49aesJXlcIXtifJBN-9ZFHqCzmChQN7PIsIyDDsrl3HJEbZ3nf1V5t3HZG2fRXUSV5nWb-WNupdWQ24zkaZtSZjg4BJ5B38ISWTqY5DoS1Emcjb16Xd-s-Y1Q9rD-dzYKOo1IEaJhLDnVYsiJvEvjlL2v4vL3Xw.z4Sm5KwSZ7kZ2K7O._nRuEt_jOmdQzvcr9I3jkeqM_pnUQ2qJXgPtQyKqpiJ0oJv9z6FzeMtX-gTiasFwO0dOcVoP48x-VrEFMqW58-kLt2npg5-PP9LD2bwyT5ItN5JBuj8VHnATQ9inOjwNdvUdmBF6YAREmm027YCOrfYciQxGCNGcZ1GrxbXgBDHacKufE9rvaXzPopsI4rlDLkdTfrsbxsw50qzSFJ5cW4O9eqax09zcCEIMioxXjN0kTEkL89ID64iFTPvoDImEpoW0xttJhmfZAcJo2Br7SBpvn4aQZBw1J46QTfRWjns1I13X4N6HyYPdVgnm2NHMk23vWxJ_1o-VH5gHR3dswnQjKSL-c-LnWn6S7yJk_DAcjlLCjtzQdH2GzKRO37zqM7qRqukfKtasB0QpAxXW2G37MXngLCqtVeUacvcPqBU3Hmu-OFYZyQCuw9sH-8RotUbXoxfAFt8UKtl1wg5g7Rdm-mEeHVMOrdFfHmBUAUrd1ua3U1Hvho_J4oPN0TTY7sUZg-pfxvz-BCnKL0lgxjusPnPdTl8_c7ah0LVb8kKS26wWAFbmLvFcOyatdi9HcAt_50asL_G85zXqDzigYLdVrq-I-jd0p4it3OZsIaMXhtYltWHl332ANIqiiU_mu-9vHofrsnWh_Va9aDcZDP5nbmXjaYc7XgZmCB939-gmCO46nYuOAISV0F3x9ULKyXpjdNDXxToiHlsisb7Mlap3HBW1Umg7zBk8Ghs5ZAq-DJeGKsySNR_VXaKgKHCWO29B0Su5woXmM6qshLGWnfEKZCyvmowKKzJHsFekRtEGtllL12TYQWu-SI6SidJILDCTSVPi_pPA1l4RWRfZRmWCvqNGVPRoi2BwHPagB4NiAfUtHJVhf1WF5iNQtP8YDgA7FEDy4pvnYmtZlYlsRlyhVpID_b3zd4NThVnDZSitp-_jZIBTld-8rUS5ddp6dqKFGr721aa_C_zoEb51S8KfCUSRrXzdVzayaUUZDY545ebVn2Fa8zw3Pjus_Sg9eFtxn7DGTfqcfb8cDxUkCKbrcqFtN5CjRmoPFmsYykBSnaKISH10VywBsAM-GJ54adELs5zJ9EVsYV80nhhV8JTHfD5KsVA1FPCBYFcTvEwRt_yS80dBrp2mVWysAa2jnzV1IxIMjdQrld0i8wPaW88p256_8hYObofxlLWTvOkAhDkZTIq8F458unoeYJad9yZGEqItc8HFLCsveNUNk7lx616II_Qyy7xNDM2E6Q1ColyyXpP8_2z7-EjlCRBEYrIXAIzNT1rVJbotlB3DhiwWq334ViUZZlDt60CSEtZTu2NuYnuyIe6CGg.N38CqdxE2SJiVfR7ygIqeA"

ECKSEN_ENDPOINT = os.environ.get("ECKSEN_ENDPOINT", "https://ecksen.com/graphql/")

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

REDIS_CLIENT = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
)
