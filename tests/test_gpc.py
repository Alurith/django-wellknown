from django.test import override_settings

GPC_PATH = "/.well-known/gpc.json"


def test_gpc_json_ok(client):
    resp = client.get(GPC_PATH)
    assert resp.status_code == 200
    data = resp.json()
    assert data["gpc"] is True
    assert data["lastUpdate"].endswith("Z")


@override_settings(WELLKNOWN_GPC=None)
def test_gpc_not_registered_when_disabled(client, reload_urls):
    reload_urls()

    resp = client.get(GPC_PATH)
    assert resp.status_code == 404
