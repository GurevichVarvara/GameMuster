"""View tests"""
from django.test import Client
from django.urls import reverse
from django.test.client import RequestFactory

from gameMuster.tests.base_test import BaseTest
from gameMuster.models import Platform, Genre
from gameMuster.views import get_game_genres, get_page_obj

ITEMS_ON_PAGE = 4


class IndexViewTestCase(BaseTest):
    """Index view tests"""
    def setUp(self):
        self.client = Client()
        self.game = self.get_game()
        self.factory = RequestFactory()
        self.platform_1 = Platform.objects.create(name='Linux')
        self.genre_1 = Genre.objects.create(name='Puzzle')
        self.game.genres.add(self.genre_1)
        self.game.platforms.add(self.platform_1)
        self.game.save()

    def test_get_page_obj(self):
        request = self.factory.get(reverse('index'))
        response = self.client.get(reverse('index'))
        page_obj = get_page_obj(request,
                                ITEMS_ON_PAGE,
                                [self.game])

        self.assertCountEqual(
            page_obj.object_list,
            response.context['page_obj'].object_list
        )

    def test_index_get(self):
        """Index view test"""
        response = self.client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameMuster/index.html')

    def test_no_filters_selected(self):
        """If no filters are selected by user"""
        response = self.client.get(reverse('index'))

        self.assertCountEqual(
            [g.id for g in response.context['game_list']],
            [self.game.id]
        )
        self.assertDictEqual(
            response.context['game_genres'],
            get_game_genres([self.game])
        )
        self.assertEqual(
            response.context['platforms_chosen'],
            None
        )
        self.assertEqual(
            response.context['genres_chosen'],
            None
        )
        self.assertEqual(response.context['rating'], 50)

    def test_filters_selected(self):
        """If filters are selected by user"""
        response = self.client.get(
            reverse('index'),
            {'platforms': [self.platform_1.id],
             'genres': [self.genre_1.id]}
        )

        self.assertCountEqual(
            [g.id for g in response.context['game_list']],
            [self.game.id]
        )
        self.assertDictEqual(
            response.context['game_genres'],
            get_game_genres([self.game])
        )
        self.assertCountEqual(
            response.context['platforms_chosen'],
            [self.platform_1.id]
        )
        self.assertCountEqual(
            response.context['genres_chosen'],
            [self.genre_1.id]
        )
        self.assertEqual(response.context['rating'], 50)
