"""Games manager tests"""
import datetime

import requests
import requests_mock
from django.conf import settings
from faker import Factory

from gameMuster.tests.base_test import BaseTest
from gameMuster.game_managers.games_manager import games_manager

from seed.factories import GameFactory

faker = Factory.create()
COUNT_OF_TWEETS_TO_LOAD = 1


class GamesManagerTestCase(BaseTest):
    """Games manager tests"""

    @requests_mock.Mocker()
    def test_generate_list_of_games(self, m):
        """Test that method returns list of games"""

        m.get(
            "https://id.twitch.tv/oauth2/"
            f"token?client_id={settings.IGDB_CLIENT_ID}"
            f"&client_secret={settings.IGDB_CLIENT_SECRET}"
            "&grant_type=client_credentials",
            json={"Client-ID": faker.pystr(), "Authorization": faker.pystr()},
        )
        m.get(
            "https://api.igdb.com/v4/games/",
            json={
                "games": [
                    {
                        "id": faker.pyint(min_value=0),
                        "name": faker.name(),
                        "summary": faker.pystr(max_chars=10),
                        "release_dates": [{"date": faker.unix_time()}],
                        "rating": faker.pyint(min_value=50, max_value=100),
                        "rating_count": faker.pyint(),
                        "aggregated_rating": faker.pyint(min_value=50, max_value=100),
                        "aggregated_rating_count": faker.pyint(),
                        "platforms": [{"name": faker.name()}],
                        "genres": [{"name": faker.name()}],
                    }
                ]
            },
        )

        response = requests.get("https://api.igdb.com/v4/games/").json()["games"][0]
        game = games_manager.get_games()[0]

        self.assertEqual(game.game_id, response["id"])
        self.assertEqual(game.name, response["name"])
        self.assertEqual(game.must, False)
        self.assertEqual(
            game.release_date,
            datetime.datetime.fromtimestamp(response["release_dates"][0]["date"]),
        )
        self.assertEqual(game.description, response["summary"])
        self.assertEqual(game.user_rating, response["rating"])
        self.assertEqual(game.user_rating_count, response["rating_count"])
        self.assertEqual(game.critics_rating, response["aggregated_rating"])
        self.assertEqual(game.critics_rating_count, response["aggregated_rating_count"])
        self.assertCountEqual(
            [platform.name for platform in game.platforms],
            [platform["name"] for platform in response["platforms"]],
        )
        self.assertCountEqual(
            [genre.name for genre in game.genres],
            [genre["name"] for genre in response["genres"]],
        )

    @requests_mock.Mocker()
    def test_create_tweets_by_game_name(self, m):
        """Test that method returns tweets related to specified game"""

        m.get(
            "https://api.twitter.com/1.1/search/tweets.json",
            json={
                "statuses": {
                    "created_at": "Fri Jun 11 12:45:10 +0000 2021",
                    "user": {"name": faker.name()},
                    "full_text": faker.pystr(max_chars=10),
                }
            },
        )

        response = requests.get(
            "https://api.twitter.com/1.1/search/tweets.json"
        ).json()["statuses"]
        tweet = games_manager.create_tweets_by_game_name(
            GameFactory(name=faker.name()), COUNT_OF_TWEETS_TO_LOAD
        )[0]

        self.assertEqual(
            tweet.date,
            datetime.datetime.strptime(
                response["created_at"], "%a %b %d %H:%M:%S %z %Y"
            ),
        )
        self.assertEqual(tweet.publisher, response["user"]["name"])
        self.assertEqual(tweet.content, response["full_text"])
