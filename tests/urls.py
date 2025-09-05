from django.http import HttpResponse
from django.urls import include, path


def dummy_change_password(request):
    return HttpResponse("ok")


urlpatterns = [
    path("", include("django_wellknown.urls")),
    path(
        "accounts/password/change/",
        dummy_change_password,
        name="account_change_password",
    ),
    path(
        "accounts/management/change_password",
        dummy_change_password,
        name="change_password",
    ),
    path("security-policy", lambda r: HttpResponse("policy")),
]
