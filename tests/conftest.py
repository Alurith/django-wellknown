import importlib
import sys

import pytest
from django.conf import settings
from django.urls import clear_url_caches


def _reload_urlconfs():
    modules = ["django_wellknown.urls", settings.ROOT_URLCONF]
    for m in modules:
        if m in sys.modules:
            importlib.reload(sys.modules[m])
    clear_url_caches()


@pytest.fixture
def reload_urls():
    _reload_urlconfs()
    yield _reload_urlconfs
    _reload_urlconfs()
