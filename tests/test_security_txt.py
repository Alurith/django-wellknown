import re

from django.test import override_settings

SECURITY_PATH = "/.well-known/security.txt"


def test_security_txt_ok(client):
    resp = client.get(SECURITY_PATH)
    assert resp.status_code == 200
    assert resp["Content-Type"].startswith("text/plain")
    body = resp.content.decode("utf-8")

    # Contact lines present (both mailto and https)
    assert "Contact: mailto:securty@example.com" in body
    assert "Contact: https://example.com/report" in body

    # Expires normalized to RFC3339 Z
    assert re.search(r"^Expires: 2026-01-01T00:00:00Z$", body, re.M), body

    # Preferred-Languages single line
    assert re.search(r"^Preferred-Languages: en, it$", body, re.M), body

    # Policy must be absolute https (path -> absolute)
    assert re.search(r"^Policy: https://example.com/security-policy$", body, re.M), body

    # Canonical must point to absolute https of this resource
    assert re.search(
        r"^Canonical: https://example.com/.well-known/security.txt$", body, re.M
    ), body


@override_settings(WELLKNOWN_SECURITY=None)
def test_security_txt_not_registered_when_disabled(client, reload_urls):
    reload_urls()

    resp = client.get(SECURITY_PATH)
    assert resp.status_code == 404
