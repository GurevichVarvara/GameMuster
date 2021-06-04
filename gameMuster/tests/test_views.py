"""View tests"""
from django.test import SimpleTestCase, Client
from django.urls import reverse


class TestViews(SimpleTestCase):
    """Test if urls call proper functions"""

    def setUp(self):
        self.client = Client()

