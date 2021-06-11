"""Games manager tests"""
import datetime

import requests
import requests_mock

from gameMuster.tests.base_test import BaseTest
from gameMuster.game_managers.games_manager import games_manager

from seed.factories import GameFactory

COUNT_OF_TWEETS_TO_LOAD = 1
GAME_NAME = "Pacman"


class GamesManagerTestCase(BaseTest):
    """Games manager tests"""

    def test_generate_list_of_games(self):
        """Test that method returns list of Game instances"""
        games = games_manager.generate_list_of_games()

    @requests_mock.Mocker()
    def test_create_tweets_by_game_name(self, m):
        """Test that method returns list of Tweet instances"""
        """Test that method returns tweets related to specified game"""

        m.get(
            "https://api.twitter.com/1.1/search/tweets.json",
            json={
                "statuses": {
                    "created_at": "Fri Jun 11 12:45:10 +0000 2021",
                    "user": {"name": "Contender eSports Hudson Valley"},
                    "full_text": "Released for arcades in 1980, the Japanese “Puck Man” was changed to “Pac-Man” "
                                 "when it went worldwide.\n#FunFactFriday\n#eSports\n#PacMan\n#RetroGaming "
                                 "https://t.co/cYLei60O5G ",
                }
            },
        )

        response = requests.get("https://api.twitter.com/1.1/search/tweets.json").json()["statuses"]
        tweet = games_manager.create_tweets_by_game_name(
            GameFactory(name=GAME_NAME),
            COUNT_OF_TWEETS_TO_LOAD
        )[0]

        self.assertEqual(
            tweet.date,
            datetime.datetime.strptime(
                response['created_at'], "%a %b %d %H:%M:%S %z %Y"
            )
        )
        self.assertEqual(tweet.publisher, response['user']['name'])
        self.assertEqual(tweet.content, response['full_text'])

