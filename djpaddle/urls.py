from django.urls import path

from . import views

app_name = "djpaddle"

urlpatterns = [
    path("webhook/", views.paddle_webhook_view, name="webhook"),
    path("checkout/", views.checkout_api_view, name="checkout_api"),
]
