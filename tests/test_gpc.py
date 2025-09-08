from django.test import Client, RequestFactory, override_settings

from django_wellknown.middleware import gpc_middleware

from .views import fake_view

GPC_PATH = "/.well-known/gpc.json"
rf = RequestFactory()


def test_gpc_json_ok(client: Client):
    resp = client.get(GPC_PATH)
    assert resp.status_code == 200
    data = resp.json()
    assert data["gpc"] is True
    assert data["lastUpdate"].endswith("Z")


@override_settings(WELLKNOWN_GPC=None)
def test_gpc_not_registered_when_disabled(client: Client, reload_urls):
    reload_urls()

    resp = client.get(GPC_PATH)
    assert resp.status_code == 404


def test_gpc_signal_present():
    mw = gpc_middleware(fake_view)

    req = rf.get("/", headers={"sec-gpc": "1"})
    res = mw(req)

    assert req.gpc is True
    assert "Sec-GPC" in res["Vary"]


def test_gpc_signal_absent():
    mw = gpc_middleware(fake_view)

    req = rf.get("/")
    res = mw(req)

    assert req.gpc is False
    assert not res.has_header("Vary")
