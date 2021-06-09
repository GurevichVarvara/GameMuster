"""View tests"""
import datetime

from django.test import Client
from django.urls import reverse
from django.test.client import RequestFactory

from gameMuster.tests.base_test import BaseTest
from gameMuster.models import Platform, Genre, Screenshot, FavoriteGame
from gameMuster.views import get_game_genres, get_page_obj

from users.models import User

ITEMS_ON_PAGE = 4


class BaseGamesViewTestCase(BaseTest):
    """Base class for games view tests"""

    def setUp(self):
        self.client = Client()
        self.game = self.get_game()
        self.factory = RequestFactory()
        self.platform_1 = Platform.objects.get_or_create(
            name='Linux'
        )[0]
        self.genre_1 = Genre.objects.get_or_create(
            name='Puzzle'
        )[0]
        self.game.genres.add(self.genre_1)
        self.game.platforms.add(self.platform_1)
        self.game.save()


class GamesIndexViewTestCase(BaseGamesViewTestCase):
    """Index view tests"""

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
            response.context['game_list'],
            [self.game]
        )
        self.assertDictEqual(
            response.context['game_genres'],
            get_game_genres([self.game])
        )
        self.assertCountEqual(
            response.context['platforms'],
            Platform.objects.all()
        )
        self.assertCountEqual(
            response.context['genres'],
            Genre.objects.all()
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
            response.context['game_list'],
            [self.game]
        )
        self.assertDictEqual(
            response.context['game_genres'],
            get_game_genres([self.game])
        )
        self.assertCountEqual(
            response.context['platforms'],
            Platform.objects.all()
        )
        self.assertCountEqual(
            response.context['genres'],
            Genre.objects.all()
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


class GamesDetailViewTestCase(BaseGamesViewTestCase):
    """Detail view tests"""

    def test_detail_get(self):
        """If game exists"""
        url = reverse('detail', args=(self.game.game_id,))
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEqual(self.game, response.context['game'])
        self.assertEqual(self.game.name.replace(' ', ''),
                         response.context['game_name'])
        self.assertCountEqual(
            list(Genre.objects.filter(game=self.game)),
            response.context['genres']
        )
        self.assertCountEqual(
            list(Platform.objects.filter(game=self.game)),
            response.context['platforms']
        )
        self.assertCountEqual(
            list(Screenshot.objects.filter(game=self.game)),
            response.context['screenshots']
        )

    def test_game_does_not_exit(self):
        """If game does not exist"""
        url = reverse('detail', args=(self.game.id + 1,))
        self.client.get(url)

        self.assertRaises(LookupError)


class FavoriteGamesViewTestCase(BaseGamesViewTestCase):
    """Favorite games view tests"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('var',
                                             'var@gmail.com',
                                             'vvva112233',
                                             active_time=datetime.datetime.now())
        self.favorite_game = FavoriteGame.objects.create(user=self.user,
                                                         game=self.game)

    def test_favorite(self):
        print(User.objects.all())
        self.client.login(username='var',
                          password='vvva112233')
        response = self.client.get(reverse('favorite'))

        self.assertEqual(response.status_code, 200)
