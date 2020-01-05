"""
sync_plans_from_paddle command.
"""
from django.core.management.base import BaseCommand

from ...models import Plan


class Command(BaseCommand):
    """Sync plans from paddle."""

    help = "Sync plans from paddle."

    def handle(self, *args, **options):
        """Call sync_from_paddle_data for each plan returned by api_list."""
        for plan_data in Plan.api_list():
            plan = Plan.sync_from_paddle_data(plan_data)
            print("Synchronized {0}".format(str(plan)))
