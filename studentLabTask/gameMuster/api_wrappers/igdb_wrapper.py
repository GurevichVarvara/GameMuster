import requests
from datetime import datetime


class IgdbWrapper:

    def __init__(self, client_id, client_secret):
        self.main_url = 'https://api.igdb.com/v4/'
        self.client_id = client_id
        self.client_secret = client_secret
        self.header = self._get_header()
        self.params_for_games = {'fields': 'id, name, cover.image_id, genres.name,'
                                           'summary, release_dates,'
                                           'aggregated_rating,'
                                           'aggregated_rating_count,'
                                           'rating, rating_count,'
                                           'screenshots.image_id,'
                                           'platforms.name',
                                 'filter[cover][not_eq]': 'null',
                                 'filter[genres][not_eq]': 'null',
                                 'filter[screenshots][not_eq]': 'null'}

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
                                 params=params)

        # if access token has expired
        if response.status_code == 401:
            self.header = self._get_header()
            response = requests.post(url,
                                     headers=self.header,
                                     params=params)

        return response.json()

    @staticmethod
    def _compose_query(default_params,
                       enumeration_filters=None,
                       rating=None):
        result_query = {**default_params}

        if enumeration_filters:
            for name, values in enumeration_filters.items():
                if not enumeration_filters[name]:
                    continue

                joined_values = ','.join(str(v) for v in values)
                result_query[f'filter[{name}][eq]'] = f'({joined_values})'

        if rating:
            result_query['filter[rating][gte]'] = rating

        return result_query

    @staticmethod
    def get_img_path(img_id):
        return 'https://images.igdb.com/igdb/' \
               f'image/upload/t_cover_big/{img_id}.jpg'

    def get_games(self, genres=None, platforms=None,
                  ids=None, rating=None):
        enumeration_filters = {'genres': genres,
                               'platforms': platforms,
                               'id': ids}

        query = self._compose_query(self.params_for_games,
                                    enumeration_filters,
                                    rating)

        games = self._post('games/', query)

        for game in games:
            game['cover'] = self.get_img_path(game['cover']['image_id'])

            if 'release_dates' in game:
                game['release_dates'] = datetime.fromtimestamp(game['release_dates'][0])
            else:
                game['release_dates'] = None

            game['rating'] = game.get('rating', None)
            game['rating_count'] = game.get('rating_count', None)
            game['aggregated_rating'] = game.get('aggregated_rating', None)
            game['aggregated_rating_count'] = game.get('aggregated_rating_count', None)

            game['screenshots'] = [self.get_img_path(screenshot['image_id']) for screenshot in
                                   game['screenshots']]
            game['platforms'] = [platform['name'] for platform
                                 in game['platforms']] if 'platforms' in game else ['All']
            game['genres'] = [genre['name'] for genre in game['genres']]

        return games

    def get_game_by_id(self, game_id):
        games = self.get_games(ids=[game_id])

        if not games:
            raise LookupError('Game not found')

        return games[0]

    def get_platforms(self):
        return self._post('platforms/',
                          self._compose_query({'fields': 'name'}))

    def get_genres(self):
        return self._post('genres/',
                          self._compose_query({'fields': 'name'}))
