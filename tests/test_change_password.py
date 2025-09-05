from urllib.parse import urlparse

from django.test import override_settings

CHANGE_PATH = "/.well-known/change-password"


def test_change_password_redirects_to_configured_url(client):
    resp = client.get(CHANGE_PATH, follow=False)
    assert resp.status_code in (301, 302, 303)
    loc = resp["Location"]
    from django.conf import settings

    print(settings.WELLKNOWN_PASSWORD_URL)

    parsed = urlparse(loc)
    print(parsed.path)
    assert parsed.path == "accounts/management/change_password/"


@override_settings(WELLKNOWN_PASSWORD=True, WELLKNOWN_PASSWORD_URL=None)
def test_change_password_redirects_to_allauth_view(client, reload_urls):
    reload_urls()

    resp = client.get(CHANGE_PATH, follow=False)
    assert resp.status_code in (301, 302, 303)
    print(resp["Location"])
