"""Twitter API wrapper"""
import datetime
import requests


class TwitterWrapper:
    """Twitter API wrapper"""
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.twitter_search_url = 'https://api.twitter.com' \
                                  '/1.1/search/tweets.json'

    def _get_header(self):
        return {'Authorization': 'Bearer {}'.format(self.bearer_token)}

    def _post(self, params=None):
        return requests.get(self.twitter_search_url,
                            headers=self._get_header(),
                            params=params).json()

    def get_tweets_by_game_name(self, game_name, count_of_tweets=3):
        """Return tweets related to game"""
        params = {'q': '%23{}'.format(game_name.replace(' ', '')),
                  'tweet_mode': 'extended',
                  'tweet.fields': 'full_text, created_at, user.name',
                  'count': count_of_tweets}

        tweets = self._post(params)['statuses']

        for tweet in tweets:
            tweet['created_at'] = datetime.datetime.strptime(tweet['created_at'],
                                                             '%a %b %d %H:%M:%S %z %Y')

        return tweets
