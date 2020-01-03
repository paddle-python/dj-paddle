from django.urls import path

from . import views

urlpatterns = [
    path("webhook/", views.paddle_webhook_view),
]
