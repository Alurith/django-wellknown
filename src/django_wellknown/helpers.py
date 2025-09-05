import datetime
from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.urls import reverse

WEB_SCHEMES = ("http", "https")
NON_WEB_SCHEMES = ("mailto:", "tel:", "dns:", "openpgp4fpr:")


def get_setting(name, default=None):
    """Fetch a Django setting or return `default` if missing.

    A trivial wrapper over `django.conf.settings` that makes it simpler to
    stub in tests.
    """
    return getattr(settings, name, default)


def abs_https(*, request, value: str) -> str:
    """Return an absolute HTTPS URI for a *web* link; preserve non-web schemes.

    Behaviour:
    - If `value` starts with a non-web scheme (e.g., `mailto:`), return it unchanged.
    - If `value` contains `://`, treat it as an absolute URI:
        * For `http`/`https`, force HTTPS and (optionally) the public host.
        * Otherwise (non-web), leave as-is.
    - If `value` starts with `/`, treat it as a site-relative path and build
      an absolute URL from the current request.
    - Otherwise, treat `value` as a Django URL **name** and `reverse()` it,
      then build an absolute URL.

    Host resolution:
    - If `settings.WELLKNOWN_HOST` is set, it is used as the public host.
    - Otherwise, `request.get_host()` is used.

    Rationale:
    RFC 9116 requires that web URIs in `security.txt` (e.g., Policy, Canonical)
    use `https://`. This helper enforces that while letting non-web schemes
    (like `mailto:`) pass through unchanged.
    """
    if any(value.startswith(s) for s in NON_WEB_SCHEMES):
        return value

    if "://" not in value:
        if value.startswith("/"):
            value = request.build_absolute_uri(value)
        else:
            value = request.build_absolute_uri(reverse(value))

    parsed = urlparse(value)
    if parsed.scheme in WEB_SCHEMES:
        host = getattr(settings, "WELLKNOWN_HOST", None)
        if host is None:
            host = parsed.netloc or request.get_host()
        value = str(urlunparse(("https", host, parsed.path, "", parsed.query, "")))
    return value


def iso8601(*, dt_str: str) -> str:
    """Normalize an input date/datetime string to RFC3339 UTC (Z) format.

    Accepts:
      - 'YYYY-MM-DD' (assumes midnight UTC)
      - ISO 8601 datetimes, with or without timezone (e.g. '2026-01-01T12:34:00',
        '2026-01-01T12:34:00+02:00', '2026-01-01T12:34:00Z').

    Returns:
      A string like 'YYYY-MM-DDTHH:MM:SSZ'.

    Raises:
      ValueError: if parsing fails.
    """
    try:
        d = datetime.datetime.fromisoformat(dt_str)
        if d.tzinfo is None:
            d = d.replace(tzinfo=datetime.timezone.utc)
        return d.astimezone(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception as e:
        raise ValueError(f"{e}. Expires must be ISO 8601 (e.g. 2026-01-01T00:00:00Z)")
