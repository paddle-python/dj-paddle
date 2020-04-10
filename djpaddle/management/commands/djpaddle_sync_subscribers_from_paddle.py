"""
sync_subscribers_from_paddle command.
"""
from django.core.management.base import BaseCommand

from ...models import Subscription


class Command(BaseCommand):
    """Sync subscribers from paddle."""

    help = "Sync subscribers from paddle."

    def handle(self, *args, **options):
        """Call sync_from_paddle_data for each subscriber returned by api_list."""
        for sub_data in Subscription.api_list():
            sub = Subscription.sync_from_paddle_data(sub_data)
            print("Synchronized {0}".format(str(sub)))
