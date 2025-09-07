from urllib.parse import urlparse

CHANGE_PATH = "/.well-known/change-password"


def test_change_password_redirects_to_configured_url(client):
    resp = client.get(CHANGE_PATH, follow=False)
    assert resp.status_code in (301, 302, 303)
    loc = resp["Location"]

    parsed = urlparse(loc)
    assert parsed.path == "/accounts/management/change_password/"
