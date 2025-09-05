SECRET_KEY = "test-secret-key"
DEBUG = True
USE_TZ = True
ALLOWED_HOSTS = ["testserver", "example.com", "localhost"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django_wellknown",
]

MIDDLEWARE = []

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {},
    }
]

STATIC_URL = "/static/"

WELLKNOWN_SECURITY = {
    "contact": ["mailto:securty@example.com", "https://example.com/report"],
    "expires": "2026-01-01",
    "policy": "/security-policy",
    "preferred_languages": "en, it",
}

WELLKNOWN_GPC = {"gpc": True, "lastUpdate": "2025-08-01"}
WELLKNOWN_PASSWORD_URL = "django_wellknown:change_password"

WELLKNOWN_HOST = "example.com"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
