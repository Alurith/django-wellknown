from django.urls import path

from django_wellknown import helpers, views

urlpatterns = []

# RFC 9116: security.txt (enabled when WELLKNOWN_SECURITY is configured)
# See https://securitytxt.org/
if helpers.get_setting("WELLKNOWN_SECURITY"):
    urlpatterns.append(
        path(".well-known/security.txt", views.security_txt, name="security_txt")
    )

# Global Privacy Control site-wide declaration
# See https://www.w3.org/TR/gpc/ and implementation guidance from GPC
if helpers.get_setting("WELLKNOWN_GPC"):
    urlpatterns.append(path(".well-known/gpc.json", views.gpc_json, name="gpc_json"))

# W3C well-known URL to help tools find the password change page
if helpers.get_setting("WELLKNOWN_PASSWORD") or helpers.get_setting(
    "WELLKNOWN_PASSWORD_URL"
):
    urlpatterns.append(
        path(
            ".well-known/change-password", views.change_password, name="change_password"
        )
    )
