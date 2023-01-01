from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
