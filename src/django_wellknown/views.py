from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from django_wellknown import helpers


@require_GET
@cache_control(max_age=60 * 60)
def security_txt(request):
    """Minimal RFC 9116 `security.txt` endpoint.

    Configuration:
      settings.WELLKNOWN_SECURITY = {
        "contact": ["mailto:security@example.com", "https://example.com/report"],
        "expires": "2026-01-01T00:00:00Z",
        # optional:
        # "policy": "https://example.com/security-policy",
        # "acknowledgments": "https://example.com/hall-of-fame" or list[str],
        # "hiring": "https://example.com/jobs",
        # "encryption": "https://example.com/pgp.txt" or "openpgp4fpr:...",
        # "csaf": "https://example.com/.well-known/csaf/metadata.json",
        # "preferred_languages": "en, it" or list[str],
      }

    Behaviour:
      - Emits `text/plain; charset=utf-8` with a 1h cache TTL.
      - Normalizes `Expires:` to RFC3339 UTC using helpers.iso8601().
      - Always includes a `Canonical:` line pointing to this endpoint's
        absolute HTTPS URL (good practice per RFC 9116).
      - Ensures that web URIs (Policy, Canonical, etc.) are **absolute HTTPS**
        using helpers.abs_https(); non-web schemes (e.g., `mailto:`) are
        preserved as-is.

    Raises:
      ValueError if required fields are missing or invalid.
    """
    cfg = helpers.get_setting("WELLKNOWN_SECURITY", {}) or {}
    lines = []

    # --- Required: Contact (one or more) ---
    contact = cfg.get("contact")
    if not contact:
        raise ValueError("Contact is required")
    contacts = contact if isinstance(contact, (list, tuple)) else [contact]
    for c in contacts:
        lines.append(f"Contact: {c}")

    # --- Required: Expires (single RFC3339 datetime) ---
    expires = cfg.get("expires")
    if not expires:
        raise ValueError("Expires is required")
    lines.append(f"Expires: {helpers.iso8601(dt_str=expires)}")

    # --- Optional: Preferred-Languages (single line, BCP47 tags) ---
    langs = cfg.get("preferred_languages")
    if isinstance(langs, str):
        langs = [s.strip() for s in langs.split(",") if s.strip()]
    if langs:
        lines.append(f"Preferred-Languages: {', '.join(langs)}")

    # --- Canonical: absolute HTTPS URL to *this* well-known resource ---
    lines.append(
        f"Canonical: {helpers.abs_https(request=request, value='security_txt')}"
    )

    # --- Optional fields that may take one or more values ---
    for key, field in {
        "policy": "Policy",
        "acknowledgments": "Acknowledgments",
        "hiring": "Hiring",
        "encryption": "Encryption",
        "csaf": "CSAF",
    }.items():
        val = cfg.get(key)
        if not val:
            continue
        vals = val if isinstance(val, (list, tuple)) else [val]
        for v in vals:
            lines.append(f"{field}: {helpers.abs_https(request=request, value=v)}")

    body = "\n".join(lines) + "\n"
    resp = HttpResponse(body, content_type="text/plain; charset=utf-8")
    return resp


@require_GET
@cache_control(max_age=60 * 60)
def gpc_json(request):
    """Global Privacy Control (GPC) site-wide declaration.

    This optional `/.well-known/gpc.json` file can be used to publicly
    declare that your site honors the GPC signal and when that policy was
    last updated. It is *advisory*; the GPC preference itself is expressed
    via the HTTP header / JS API as per the W3C draft.

    Configure with:
      settings.WELLKNOWN_GPC = {"gpc": True, "lastUpdate": "YYYY-MM-DD"}

    Behaviour:
      - Ensures `gpc` key is present (defaults to False if omitted).
      - Normalizes `lastUpdate` to RFC3339 UTC via helpers.iso8601().
      - Responds with a compact JSON body and 1h cache TTL.

    Raises:
      ValueError if `lastUpdate` is missing or invalid.
    """
    cfg = dict(helpers.get_setting("WELLKNOWN_GPC"))

    cfg.setdefault("gpc", False)

    last_update = cfg.get("lastUpdate", None)
    if not last_update:
        raise ValueError("lastUpdate is required")
    cfg["lastUpdate"] = helpers.iso8601(dt_str=last_update)
    resp = JsonResponse(cfg)
    return resp


@require_GET
def change_password(request):
    """Redirect to the site's change-password form (W3C well-known URL).

    Usage options:
      1) If you use django-allauth, set:
         settings.WELLKNOWN_PASSWORD = True
         (This view will reverse 'account_change_password'.)
      2) Otherwise set:
         settings.WELLKNOWN_PASSWORD_URL = "/account/password/change/"
         or a fully-qualified HTTPS URL.

    Behaviour:
      - Tries to reverse the canonical change-password view first (allauth).
      - Falls back to WELLKNOWN_PASSWORD_URL.
      - Ensures we redirect to an absolute HTTPS URL using helpers.abs_https().

    Returns:
      302/303 redirect (HttpResponseRedirect) to the effective change-password URL.

    Raises:
      ValueError if neither allauth route nor WELLKNOWN_PASSWORD_URL is available.
    """
    try:
        url = reverse("account_change_password")
    except NoReverseMatch:
        url = helpers.get_setting("WELLKNOWN_PASSWORD_URL")
        if not url:
            raise ValueError("WELLKNOWN_PASSWORD_URL is required")

        url = helpers.abs_https(request=request, value=url)

    return HttpResponseRedirect(url)
