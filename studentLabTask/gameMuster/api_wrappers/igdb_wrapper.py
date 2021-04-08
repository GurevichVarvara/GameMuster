import requests
from datetime import datetime


class IgdbWrapper:

    def __init__(self, client_id, client_secret):
        self.main_url = 'https://api.igdb.com/v4/'
        self.client_id = client_id
        self.client_secret = client_secret
        self.header = self._get_header()

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
    def get_img_path(img_id):
        return 'https://images.igdb.com/igdb/' \
               f'image/upload/t_cover_big/{img_id}.jpg'

    def get_games(self, additional_params=None):
        params = {'fields': 'id, name, cover.image_id, genres.name,'
                            'summary, release_dates,'
                            'aggregated_rating,'
                            'aggregated_rating_count,'
                            'rating, rating_count,'
                            'screenshots.image_id,'
                            'platforms.name',
                  'filter[cover][not_eq]': 'null',
                  'filter[genres][not_eq]': 'null',
                  'filter[screenshots][not_eq]': 'null',
                  **additional_params}

        games = self._post('games/', params)

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
                                 in game['platforms']]
            game['genres'] = [genre['name'] for genre in game['genres']]

        return games

    def get_platforms(self, params=None):
        return self._post('platforms/', params)

    def get_genres(self, params=None):
        return self._post('genres/', params)
