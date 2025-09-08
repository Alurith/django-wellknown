from urllib.parse import urlparse

from django.test import override_settings

CHANGE_PATH = "/.well-known/change-password"


def test_change_password_redirects_to_configured_url(client):
    resp = client.get(CHANGE_PATH, follow=False)
    assert resp.status_code in (301, 302, 303)
    loc = resp["Location"]

    parsed = urlparse(loc)
    assert parsed.path == "/accounts/password/change/"


@override_settings(WELLKNOWN_PASSWORD=True, WELLKNOWN_PASSWORD_URL=None)
def test_change_password_redirects_to_allauth_view(client, reload_urls):
    reload_urls()

    resp = client.get(CHANGE_PATH, follow=False)
    assert resp.status_code in (301, 302, 303)
