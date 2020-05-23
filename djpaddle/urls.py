from django.urls import path

from . import views

app_name = "djpaddle"

urlpatterns = [
    path("webhook/", views.paddle_webhook_view, name="webhook"),
    path("post-checkout/", views.post_checkout_api_view, name="post_checkout_api"),
]
