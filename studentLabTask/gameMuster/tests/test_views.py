from django.test import SimpleTestCase, Client
from django.urls import reverse
from gameMuster.temp_models import ModelManager


class TestViews(SimpleTestCase):
    """Tests for views

    Tests if urls call proper functions.
    """

    def setUp(self):
        self.client = Client()

    def test_index_GET(self):
        response = self.client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameMuster/index.html')

    def test_detail_GET(self):
        response = self.client.get(reverse('detail', args=(1,)))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameMuster/detail.html')