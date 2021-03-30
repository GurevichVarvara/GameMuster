from django.test import SimpleTestCase
from django.urls import resolve, reverse
from gameMuster.views import index, detail


class TestUrls(SimpleTestCase):
    """Tests for urls

    Tests if urls call proper functions.
    """

    def test_index_url_resolves(self):
        url = reverse('index')

        self.assertEquals(resolve(url).func, index)

    def test_delail_url_resolves(self):
        url = reverse('detail')

        self.assertEquals(resolve(url).func, detail)
