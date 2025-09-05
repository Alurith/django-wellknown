from django.conf import settings
from django.urls import path

from django_wellknown import views

urlpatterns = []

if getattr(settings, "WELLKNOWN_SECURITY", None):
    urlpatterns.append(
        path(".well-known/security.txt", views.security_txt, name="security_txt"),
    )
