from django.contrib import admin

from . import models

admin.site.register(models.Checkout)


class PriceInline(admin.TabularInline):
    model = models.Price


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    inlines = (PriceInline,)
    list_display = (
        "id",
        "name",
    )


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "subscriber",
        "email",
        "status",
        "plan",
    )
    list_filter = (
        "status",
        "plan",
    )
