# django-wellknown

Expose selected `/.well-known/*` endpoints in Django (per RFC 8615). This package focuses on small, standards‑compliant views you can drop into any project.

**Implemented endpoints**

* `/.well-known/security.txt` — vulnerability disclosure metadata (RFC 9116)
* `/.well-known/change-password` — discovery URL for password‑change forms (W3C)
* `/.well-known/gpc.json` — site‑wide Global Privacy Control declaration (W3C draft)

## Installation

```bash
pip install "git+https://github.com/Alurith/django-wellknown.git"
# or (uv)
uv pip install "git+https://github.com/Alurith/django-wellknown.git"
```

Add the app and URLconf:

```python
# settings.py
INSTALLED_APPS = [
    # ...
    "django_wellknown",  # or "django_wellknown.app.WellKnownConfig"
]
```

```python
# urls.py
from django.urls import include, path

urlpatterns = [
    path("", include("django_wellknown.urls")),
]
```

The URLconf registers endpoints **only** when their corresponding settings are present (see below).


## Quick start

### 1) `/.well-known/security.txt` (RFC 9116)

Add your disclosure details to settings:

```python
# settings.py
WELLKNOWN_SECURITY = {
    # REQUIRED — one or more contacts (order by preference):
    "contact": [
        "mailto:security@example.com",
        "https://example.com/vulnerability-report",
    ],
    # REQUIRED — RFC3339 date/time after which data is stale (UTC recommended):
    "expires": "2026-01-01T00:00:00Z",

    # OPTIONAL:
    "policy": "https://example.com/security-policy",
    "acknowledgments": "https://example.com/hall-of-fame",
    "hiring": "https://example.com/jobs",
    # can also be "openpgp4fpr:..." or a mail address hosting a key:
    "encryption": "https://example.com/pgp.txt",
    "csaf": "https://example.com/.well-known/csaf/metadata.json",
    # BCP47/RFC5646 tags — string "en, it" or list ["en", "it"]:
    "preferred_languages": "en, it",
}
```

Start the server and visit:

```
https://<your-host>/.well-known/security.txt
```


### 2) `/.well-known/change-password` (W3C)

Enable one of the following:

```python
# Option A: you use django-allauth; the view name will be reversed.
WELLKNOWN_PASSWORD = True

# Option B: provide your own URL or URL name.
WELLKNOWN_PASSWORD_URL = "/accounts/password/change/"
# or a fully-qualified HTTPS URL, e.g. "https://example.com/accounts/password/change/"
```

Hitting `/.well-known/change-password` will **redirect** to your change form. This follows the W3C spec so password managers can find the form reliably.


### 3) `/.well-known/gpc.json` (Global Privacy Control)

Declare site‑wide support for GPC:

```python
WELLKNOWN_GPC = {
    "gpc": True,                   # site abides by GPC requests (advisory resource)
    "lastUpdate": "2025-08-01",   # normalized to RFC3339 UTC
}
```

Visit `/.well-known/gpc.json`. The GPC support resource lets your site advertise that it recognizes and honors the GPC signal; the actual user preference is conveyed via HTTP header / JS API.


## Settings reference

```python
# REQUIRED to enable security.txt
WELLKNOWN_SECURITY: dict = {
    "contact": str | list[str],          # one or more; mailto:, https://, etc.
    "expires": str,                      # RFC3339 or YYYY-MM-DD (will be normalized)
    # optional fields:
    "policy": str | list[str],
    "acknowledgments": str | list[str],
    "hiring": str | list[str],
    "encryption": str | list[str],
    "canonical": str | list[str],
    "csaf": str | list[str],
    "preferred_languages": str | list[str],
}

# OPTIONAL: W3C change-password endpoint
WELLKNOWN_PASSWORD: bool = False          # try to reverse 'account_change_password'
WELLKNOWN_PASSWORD_URL: str | None = None # fallback path/URL if not using allauth

# OPTIONAL: GPC declaration
WELLKNOWN_GPC: dict = {"gpc": True, "lastUpdate": "YYYY-MM-DD"}

# OPTIONAL: public host override when building absolute URLs behind a proxy
WELLKNOWN_HOST: str | None = None
```

## Development

```bash
git clone https://github.com/Alurith/django-wellknown.git
cd django-wellknown
pip install -e .
# run your demo project or tests as desired
```

## License

MIT
