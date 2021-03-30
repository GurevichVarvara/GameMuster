from django.test import SimpleTestCase, Client
from django.urls import reverse


class TestViews(SimpleTestCase):
    """Tests for views

    Tests if urls call proper functions.
    """

    def test_index_GET(self):
        client = Client()
        response = client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameMuster/index.html')

    def test_detail_GET(self):
        client = Client()
        response = client.get(reverse('detail'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameMuster/detail.html')