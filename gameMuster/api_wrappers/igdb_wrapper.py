import requests
from datetime import datetime
from django.http import HttpResponseServerError


class IgdbWrapper:

    def __init__(self, client_id, client_secret):
        self.main_url = 'https://api.igdb.com/v4/'
        self.client_id = client_id
        self.client_secret = client_secret
        self.header = self._get_header()
        self.base_fields = 'fields game.id, game.name, game.cover.image_id, ' \
                           'game.genres.name, game.summary, game.release_dates, ' \
                           'game.aggregated_rating, game.aggregated_rating_count, ' \
                           'game.rating, game.rating_count, ' \
                           'game.screenshots.image_id, game.platforms.name;'
        self.base_filters = 'where game.cover != null & game.genres != null & game.rating != null & ' \
                            'game.aggregated_rating != null & game.screenshots != null'

    def _get_header(self):
        response = requests.post('https://id.twitch.tv/oauth2/'
                                 f'token?client_id={self.client_id}'
                                 f'&client_secret={self.client_secret}'
                                 '&grant_type=client_credentials')

        if response.status_code == 401:
            raise Exception('Incorrect client id or client secret')

        return {'Client-ID': self.client_id,
                'Authorization': 'Bearer {}'.format(response.json()['access_token'])}

    def _post(self, endpoint, params=None):
        url = self.main_url + endpoint

        response = requests.post(url,
                                 headers=self.header,
                                 data=params)

        # if access token has expired
        if response.status_code == 401:
            self.header = self._get_header()
            response = requests.post(url,
                                     headers=self.header,
                                     data=params)

        if not response.ok:
            raise HttpResponseServerError

        return response.json()

    def _request_latest_game_dates(self,
                                   last_release_date=None,
                                   count_of_games=None):
        endpoint = 'release_dates/'
        query = 'fields game.id, date;' + \
                self.base_filters

        if last_release_date:
            query += f' & date > {int(last_release_date.timestamp())}'

        query += '; sort date asc;'

        if count_of_games:
            query += f'limit {count_of_games};'

        return {result['game']['id']: datetime.fromtimestamp(result['date'])
                for result in self._post(endpoint, query)}

    def _request_games(self,
                       default_params,
                       enumeration_filters=None,
                       rating=None):
        endpoint = 'games/'
        query = default_params

        if enumeration_filters:
            for name, values in enumeration_filters.items():
                if not enumeration_filters[name]:
                    continue

                joined_values = ','.join(str(v) for v in values)
                query += f' & {name} = ({joined_values})'

        if rating:
            query += f' & rating >= {rating}'

        query += ';'

        return self._post(endpoint, query)

    @staticmethod
    def get_img_path(img_id):
        return 'https://images.igdb.com/igdb/' \
               f'image/upload/t_cover_big/{img_id}.jpg'

    def get_games(self,
                  genres=None,
                  platforms=None,
                  rating=None,
                  last_release_date=None,
                  count_of_games=None):
        latest_game_dates = self._request_latest_game_dates(last_release_date, count_of_games)
        enumeration_filters = {'genres': genres,
                               'platforms': platforms,
                               'id': list(latest_game_dates.keys())}
        games = self._request_games(default_params=self.base_fields.replace('game.', '') +
                                                   self.base_filters.replace('game.', ''),
                                    enumeration_filters=enumeration_filters,
                                    rating=rating)

        for game in games:
            game['cover'] = self.get_img_path(game['cover']['image_id'])

            game['release_dates'] = latest_game_dates[game['id']]
            game['rating'] = game.get('rating', None)
            game['rating_count'] = game.get('rating_count', None)
            game['aggregated_rating'] = game.get('aggregated_rating', None)
            game['aggregated_rating_count'] = game.get('aggregated_rating_count', None)

            game['screenshots'] = [self.get_img_path(screenshot['image_id']) for screenshot in
                                   game['screenshots']]
            game['platforms'] = [platform['name'] for platform
                                 in game['platforms']] if 'platforms' in game else None
            game['genres'] = [genre['name'] for genre in game['genres']]

        return games
