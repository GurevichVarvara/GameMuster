"""View tests"""
from django.test import SimpleTestCase, Client
from django.urls import reverse


class TestViews(SimpleTestCase):
    """Test if urls call proper functions"""

    def setUp(self):
        self.client = Client()

    def test_index_get(self):
        """Index view test"""
        response = self.client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameMuster/index.html')

    def test_detail_get(self):
        """Detail view test"""
        response = self.client.get(reverse('detail', args=(1,)))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameMuster/detail.html')
