"""View tests"""
from django.test import Client
from django.urls import reverse

from gameMuster.tests.base_test import BaseTest
from gameMuster.models import Platform, Genre, Game


class IndexViewTestCase(BaseTest):
    """View tests"""

    def setUp(self):
        self.client = Client()
        self.game = self.get_game()
        self.platform_1 = Platform.objects.create(name='Linux')
        self.genre_1 = Genre.objects.create(name='Puzzle')
        self.game.genres.add(self.genre_1)
        self.game.platforms.add(self.platform_1)
        self.game.save()

    def test_index_get(self):
        """Index view test"""
        response = self.client.get(reverse('index'),
                                   {'platforms': ['1', '2'],
                                    'genres': ['1']})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameMuster/index.html')

    def test_no_filters_selected(self):
        """If no filters are selected by user"""
        response = self.client.get(reverse('index'))

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
        self.assertCountEqual(
            [platform for platform in response.context['platforms_chosen']],
            [self.platform_1.id]
        )
        self.assertCountEqual(
            [genre for genre in response.context['genres_chosen']],
            [self.genre_1.id]
        )
        self.assertEqual(response.context['rating'], 50)
