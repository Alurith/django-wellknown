from django.urls import path

from django_wellknown import helpers, views

urlpatterns = []

if helpers.get_setting("WELLKNOWN_SECURITY"):
    urlpatterns.append(
        path(".well-known/security.txt", views.security_txt, name="security_txt")
    )
if helpers.get_setting("WELLKNOWN_GPC"):
    urlpatterns.append(path(".well-known/gpc.json", views.gpc_json, name="gpc_json"))

if helpers.get_setting("WELLKNOWN_PASSWORD") or helpers.get_setting(
    "WELLKNOWN_PASSWORD_URL"
):
    urlpatterns.append(
        path(
            ".well-known/change-password", views.change_password, name="change_password"
        )
    )
