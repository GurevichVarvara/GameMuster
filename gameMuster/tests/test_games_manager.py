"""Games manager tests"""
import datetime
import re

import requests
import requests_mock

from gameMuster.tests.base_test import BaseTest
from gameMuster.game_managers.games_manager import games_manager

from seed.factories import GameFactory

COUNT_OF_TWEETS_TO_LOAD = 1
adapter = requests_mock.Adapter()
session = requests.Session()
session.mount("https://", adapter)


class GamesManagerTestCase(BaseTest):
    """Games manager tests"""

    def test_generate_list_of_games(self):
        """Test that method returns list of games"""

        game_pattern = re.compile("https://api.igdb.com/v4/games/")
        adapter.register_uri(
            "GET",
            game_pattern,
            json={
                "games": [
                    {
                        "id": self.faker.pyint(min_value=0),
                        "name": self.faker.name(),
                        "summary": self.faker.pystr(max_chars=10),
                        "release_dates": [{"date": self.faker.unix_time()}],
                        "rating": self.faker.pyint(min_value=50, max_value=100),
                        "rating_count": self.faker.pyint(),
                        "aggregated_rating": self.faker.pyint(
                            min_value=50, max_value=100
                        ),
                        "aggregated_rating_count": self.faker.pyint(),
                        "platforms": [{"name": self.faker.name()}],
                        "genres": [{"name": self.faker.name()}],
                    }
                ]
            },
        )

        response = session.get("https://api.igdb.com/v4/games/").json()["games"][0]
        game = games_manager.generate_list_of_games()[0]

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

    def test_create_tweets_by_game_name(self):
        """Test that method returns tweets related to specified game"""

        tweet_pattern = re.compile("https://api.twitter.com/1.1/search/tweets.json")
        adapter.register_uri(
            "GET",
            tweet_pattern,
            json={
                "statuses": {
                    "created_at": "Fri Jun 11 12:45:10 +0000 2021",
                    "user": {"name": self.faker.name()},
                    "full_text": self.faker.pystr(max_chars=10),
                }
            },
        )

        response = session.get("https://api.twitter.com/1.1/search/tweets.json").json()[
            "statuses"
        ]
        tweet = games_manager.create_tweets_by_game_name(
            GameFactory(name=self.faker.name()), COUNT_OF_TWEETS_TO_LOAD
        )[0]

        self.assertEqual(
            tweet.date,
            datetime.datetime.strptime(
                response["created_at"], "%a %b %d %H:%M:%S %z %Y"
            ),
        )
        self.assertEqual(tweet.publisher, response["user"]["name"])
        self.assertEqual(tweet.content, response["full_text"])
