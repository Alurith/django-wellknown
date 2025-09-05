import datetime
from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.urls import reverse

WEB_SCHEMES = ("http", "https")
NON_WEB_SCHEMES = ("mailto:", "tel:", "dns:", "openpgp4fpr:")


def get_setting(name, default=None):
    return getattr(settings, name, default)


def abs_https(*, request, value: str) -> str:
    """
    Returns an absolute https URI (if it's a web URI).
        - If value is a urlpattern name -> reverse() + build_absolute_uri()
        - If value is a path -> build_absolute_uri()
        - If it's already an absolute URI:
        - For http/https, force https (RFC 9116 requires https)
        - For mailto/tel/dns/openpgp4fpr, leave unchanged
    You can force the host with settings.WELLKNOWN_HOST if behind a proxy.
    """
    if any(value.startswith(s) for s in NON_WEB_SCHEMES):
        return value

    if "://" not in value:
        # path o nome di route
        if value.startswith("/"):
            value = request.build_absolute_uri(value)
        else:
            value = request.build_absolute_uri(reverse(value))

    parsed = urlparse(value)
    if parsed.scheme in WEB_SCHEMES:
        host = parsed.netloc or getattr(settings, "WELLKNOWN_HOST", "")
        if not host:
            host = request.get_host()
        value = str(urlunparse(("https", host, parsed.path, "", parsed.query, "")))
    return value


def iso8601(*, dt_str: str) -> str:
    try:
        d = datetime.datetime.fromisoformat(dt_str)
        if d.tzinfo is None:
            d = d.replace(tzinfo=datetime.timezone.utc)
        return d.astimezone(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception as e:
        raise ValueError(f"{e}. Expires must be ISO 8601 (e.g. 2026-01-01T00:00:00Z)")
