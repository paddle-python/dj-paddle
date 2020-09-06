from django.test.testcases import TestCase

from djpaddle import settings, mappers


class TestPaddleMappers(TestCase):
    def test_subscriber_by_payload(self):
        Subscriber = settings.get_subscriber_model()
        payload = {"email": "nonexistent@email.com"}

        with self.assertRaises(Subscriber.DoesNotExist):
            mappers.get_subscriber_by_payload(Subscriber, payload)
