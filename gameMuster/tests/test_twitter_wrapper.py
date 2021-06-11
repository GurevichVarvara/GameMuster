"""Twitter API wrapper tests"""
import datetime
import os

import requests
import requests_mock

from django.conf import settings

from gameMuster.tests.base_test import BaseTest
from gameMuster.api_wrappers.twitter_wrapper import TwitterWrapper

COUNT_OF_TWEETS_TO_LOAD = 1
TWEET_NAME = "Pacman"


class TwitterWrapperTestCase(BaseTest):
    """Twitter API wrapper tests"""

    twitter_wrapper = TwitterWrapper(os.getenv("TWITTER_BEARER_TOKEN"))

    @requests_mock.Mocker()
    def test_get_tweets_by_game_name(self, m):
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

        self.assertEqual(
            requests.get("https://api.twitter.com/1.1/search/tweets.json").json()[
                "statuses"
            ]["user"]["name"],
            "Contender eSports Hudson Valley",
        )

        tweets = self.twitter_wrapper.get_tweets_by_game_name(
            game_name=TWEET_NAME, count_of_tweets=COUNT_OF_TWEETS_TO_LOAD
        )
