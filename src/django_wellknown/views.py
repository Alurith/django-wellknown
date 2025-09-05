from django.conf import settings
from django.http import (
    HttpResponse,
    JsonResponse,
)

from django_wellknown import helpers


def _get_setting(name, default=None):
    return getattr(settings, name, default)


def security_txt(request):
    cfg = _get_setting("WELLKNOWN_SECURITY", {}) or {}
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
    resp["Cache-Control"] = "max-age=3600"
    return resp


def gpc_json(request):
    """Global Privacy Control declaration.


    settings.WELLKNOWN_GPC = {"gpc": True, "lastUpdate": "YYYY-MM-DD"}
    """
    cfg = dict(_get_setting("WELLKNOWN_GPC"))

    cfg.setdefault("gpc", False)

    last_update = cfg.get("lastUpdate", None)
    if not last_update:
        raise ValueError("lastUpdate is required")
    cfg["lastUpdate"] = helpers.iso8601(dt_str=last_update)
    resp = JsonResponse(cfg)
    resp["Cache-Control"] = "max-age=3600"
    return resp
