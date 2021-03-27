from django.test import SimpleTestCase, Client
from django.urls import reverse


class TestViews(SimpleTestCase):
    """Tests for views

    Tests if urls call proper functions.
    """

    def test_index_GET(self):
        client = Client()
        response = client.get(reverse('index'))
        print(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameMuster/index.html')