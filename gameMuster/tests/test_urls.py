"""Url tests"""
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from gameMuster.views import index, detail


class TestUrls(SimpleTestCase):
    """Test if urls call proper functions"""

    def test_index_url_resolves(self):
        """Index url test"""
        url = reverse('index')

        self.assertEquals(resolve(url).func, index)

    def test_detail_url_resolves(self):
        """Detail url test"""
        url = reverse('detail', args=(1,))

        self.assertEquals(resolve(url).func, detail)
