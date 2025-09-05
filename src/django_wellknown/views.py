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
    cfg = helpers.get_setting("WELLKNOWN_SECURITY", {}) or {}
    lines = []

    contact = cfg.get("contact")
    if not contact:
        raise ValueError("Contact is required")
    contacts = contact if isinstance(contact, (list, tuple)) else [contact]
    for c in contacts:
        lines.append(f"Contact: {c}")

    expires = cfg.get("expires")
    if not expires:
        raise ValueError("Expires is required")
    lines.append(f"Expires: {helpers.iso8601(dt_str=expires)}")

    langs = cfg.get("preferred_languages")
    if isinstance(langs, str):
        langs = [s.strip() for s in langs.split(",") if s.strip()]
    if langs:
        lines.append(f"Preferred-Languages: {', '.join(langs)}")

    lines.append(
        f"Canonical: {helpers.abs_https(request=request, value='security_txt')}"
    )

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
    """Global Privacy Control declaration.


    settings.WELLKNOWN_GPC = {"gpc": True, "lastUpdate": "YYYY-MM-DD"}
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
    """Redirect a change password page.

    Use settings.WELLKNOWN_PASSWORD_URL = "/account/password/change/" (or a view) to enable the redirect.

    Use settings.WELLKNOWN_PASSWORD = True with django-allauth to enable the redirect on "account_change_password"
    """
    try:
        url = reverse("account_change_password")
    except NoReverseMatch as _e:
        url = helpers.get_setting("WELLKNOWN_PASSWORD_URL")
        if not url:
            raise ValueError("WELLKNOWN_PASSWORD_URL is required")

        url = helpers.abs_https(request=request, value=url)

    return HttpResponseRedirect(url)
