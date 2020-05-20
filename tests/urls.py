from django.contrib import admin
from django.http.response import HttpResponse
from django.urls import include, path

admin.autodiscover()


def empty_view(request):
    return HttpResponse()


urlpatterns = [
    path("home/", empty_view, name="home"),
    path("admin/", admin.site.urls),
    path("djpaddle/", include(("djpaddle.urls", "djpaddle"), namespace="djpaddle")),
]
