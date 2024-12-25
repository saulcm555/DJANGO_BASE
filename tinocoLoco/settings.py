from pathlib import Path

import os
import environ
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(DEBUG=(bool, False))

env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps de terceros
    "cloudinary",
    "crispy_forms",
    "crispy_bootstrap5",
    "import_export",
    "cloudinary_storage",
    # Apps propias
    "negocio.apps.NegocioConfig",
    "eventos.apps.EventosConfig",
    "alquileres.apps.AlquileresConfig",
    "servicios.apps.ServiciosConfig",
    "usuarios.apps.UsuariosConfig",
    "core.apps.CoreConfig",
]

CRISPY_TEMPLATE_PACK = "bootstrap5"

JAZZMIN_SETTINGS = {
    "site_title": "Tinocoloco Admin",
    "site_header": "Tinocoloco",
    "site_brand": "Tinocoloco",
    "site_logo": None,
    "login_logo": None,
    "login_logo_dark": None,
}


# Configuración de Cloudinary
cloudinary.config(
    cloud_name="dj34q6boj",
    api_key="179729115289615",
    api_secret="fqwB9EsbAEpSjl9whJGGRCmjqDw",
        secure=True,
    debug=True,
)
CLOUDINARY_URL = "cloudinary://179729115289615:fqwB9EsbAEpSjl9whJGGRCmjqDw@dj34q6boj"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tinocoLoco.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.contex_processors.configuracion_negocio_context",
                "core.contex_processors.eventos_mas_gustados_context",
            ],
        },
    },
]

WSGI_APPLICATION = "tinocoLoco.wsgi.application"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "saulcmtrabajos@gmail.com"
EMAIL_HOST_PASSWORD = "fdcutlymsupkyrgt"
DEFAULT_FROM_EMAIL = "TinocoLoco@gmail"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "es"


TIME_ZONE = "America/Guayaquil"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/



# Archivos estáticos
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Carpeta donde trabajas con archivos estáticos locales
]
STATIC_ROOT = BASE_DIR / "staticfiles"  

# Archivos multimedia
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGIN_URL = "usuarios:iniciar_sesion"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "usuarios:iniciar_sesion"
