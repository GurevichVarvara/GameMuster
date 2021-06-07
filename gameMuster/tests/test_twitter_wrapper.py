"""Twitter API wrapper tests"""
from django.conf import settings

from gameMuster.tests.base_test import BaseTest
from gameMuster.api_wrappers.twitter_wrapper import TwitterWrapper

COUNT_OF_TWEETS_TO_LOAD = 5
TWEET_NAME = 'Pacman'


class TwitterWrapperTestCase(BaseTest):
    """Twitter API wrapper tests"""
    twitter_wrapper = TwitterWrapper(settings.TWITTER_BEARER_TOKEN)

    def test_get_header(self):
        """Test that method returns header with proper fields"""
        header = self.twitter_wrapper._get_header()

        self.assertIsInstance(header, dict)
        self.assertIn('Authorization', header)

    def test_get_tweets_by_game_name(self):
        """Test that method returns tweets related to specified game"""
        tweets = self.twitter_wrapper.get_tweets_by_game_name(
            TWEET_NAME,
            COUNT_OF_TWEETS_TO_LOAD)
        tweet_fields = ['full_text', 'created_at', 'user']

        self.check_list(tweets, dict)
        self.assertEqual(len(tweets), COUNT_OF_TWEETS_TO_LOAD)

        for field in tweet_fields:
            self.assertIn(field, tweets[0])
