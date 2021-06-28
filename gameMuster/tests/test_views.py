"""View tests"""
import requests_mock
from django.urls import reverse

from gameMuster.tests.base_test import BaseTest
from gameMuster.models import Platform, Genre, Screenshot, FavoriteGame
from gameMuster.views import get_game_genres, get_page_obj

ITEMS_ON_PAGE = 4


class GamesIndexViewTestCase(BaseTest):
    """Index view tests"""

    def test_get_page_obj(self):
        request = self.factory.get(reverse("index"))
        response = self.client.get(reverse("index"))
        page_obj = get_page_obj(request, ITEMS_ON_PAGE, [self.game])

        self.assertCountEqual(
            page_obj.object_list, response.context["page_obj"].object_list
        )

    def test_index_get(self):
        """Index view test"""
        response = self.client.get(reverse("index"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "gameMuster/index.html")

    def test_no_filters_selected(self):
        """If no filters are selected by user"""
        response = self.client.get(reverse("index"))

        self.assertCountEqual(response.context["game_list"], [self.game])
        self.assertDictEqual(
            response.context["game_genres"], get_game_genres([self.game])
        )
        self.assertCountEqual(response.context["platforms"], Platform.objects.all())
        self.assertCountEqual(response.context["genres"], Genre.objects.all())
        self.assertEqual(response.context["platforms_chosen"], None)
        self.assertEqual(response.context["genres_chosen"], None)
        self.assertEqual(response.context["rating"], 50)

    def test_filters_selected(self):
        """If filters are selected by user"""
        response = self.client.get(
            reverse("index"),
            {"platforms": [self.platform.id], "genres": [self.genre.id], "rating": 0},
        )

        self.assertCountEqual(response.context["game_list"], [self.game])
        self.assertDictEqual(
            response.context["game_genres"], get_game_genres([self.game])
        )
        self.assertCountEqual(response.context["platforms"], Platform.objects.all())
        self.assertCountEqual(response.context["genres"], Genre.objects.all())
        self.assertCountEqual(response.context["platforms_chosen"], [self.platform.id])
        self.assertCountEqual(response.context["genres_chosen"], [self.genre.id])
        self.assertEqual(response.context["rating"], 0)


class GamesDetailViewTestCase(BaseTest):
    """Detail view tests"""

    @requests_mock.Mocker()
    def test_detail_get(self, mock):
        """If game exists"""
        mock.get(
            "https://api.twitter.com/1.1/search/tweets.json",
            json={
                "statuses": {
                    "created_at": "Fri Jun 11 12:45:10 +0000 2021",
                    "user": {"name": self.faker.name()},
                    "full_text": self.faker.pystr(max_chars=10),
                }
            },
        )
        url = reverse("detail", args=(self.game.game_id,))
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEqual(self.game, response.context["game"])
        self.assertEqual(self.game.name.replace(" ", ""), response.context["game_name"])
        self.assertCountEqual(
            list(Genre.objects.filter(game=self.game)), response.context["genres"]
        )
        self.assertCountEqual(
            list(Platform.objects.filter(game=self.game)), response.context["platforms"]
        )
        self.assertCountEqual(
            list(Screenshot.objects.filter(game=self.game)),
            response.context["screenshots"],
        )

    def test_game_does_not_exit(self):
        """If game does not exist"""
        url = reverse("detail", args=(self.game.id + 1,))
        self.client.get(url)

        self.assertRaises(LookupError)


class FavoriteGamesViewTestCase(BaseTest):
    """Favorite games view tests"""

    def setUp(self):
        super().setUp()
        self.login_user()

    def add_game_to_favorite(self):
        return FavoriteGame.objects.create(game=self.game, user=self.user)

    def test_favorite_authenticated(self):
        """Favorite main page test if user is authenticated"""
        favorite_game = self.add_game_to_favorite()
        response = self.client.get(reverse("favorite"))

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual([favorite_game.game], response.context["game_list"])
        self.assertCountEqual(
            [favorite_game.game.game_id], response.context["favorite_game_list"]
        )

    def test_favorite_not_authenticated(self):
        """Favorite main page test if user is not authenticated"""
        self.client.logout()
        response = self.client.get(reverse("favorite"))

        self.assertEqual(response.status_code, 302)
