from django.conf import settings
from django.urls import path

from django_wellknown import views

urlpatterns = []

if getattr(settings, "WELLKNOWN_SECURITY", None):
    urlpatterns.append(
        path(".well-known/security.txt", views.security_txt, name="security_txt")
    )
if getattr(settings, "WELLKNOWN_GPC", None):
    urlpatterns.append(path(".well-known/gpc.json", views.gpc_json, name="gpc_json"))

if getattr(settings, "WELLKNOWN_PASSWORD", None) or getattr(
    settings, "WELLKNOWN_PASSWORD_URL", None
):
    urlpatterns.append(
        path(
            ".well-known/change-password", views.change_password, name="change_password"
        )
    )
