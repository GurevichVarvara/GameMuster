import requests
from datetime import datetime
from django.http import HttpResponseServerError


class IgdbWrapper:

    def __init__(self, client_id, client_secret):
        self.main_url = 'https://api.igdb.com/v4/'
        self.client_id = client_id
        self.client_secret = client_secret
        self.header = self._get_header()
        self.default_params = {'fields': ['id', 'name', 'cover.image_id',
                                          'genres.name', 'summary', 'release_dates.date',
                                          'aggregated_rating', 'aggregated_rating_count',
                                          'rating', 'rating_count',
                                          'screenshots.image_id', 'platforms.name']}

    def _get_header(self):
        response = requests.post('https://id.twitch.tv/oauth2/'
                                 f'token?client_id={self.client_id}'
                                 f'&client_secret={self.client_secret}'
                                 '&grant_type=client_credentials')

        if response.status_code == 401:
            raise Exception('Incorrect client id or client secret')

        return {'Client-ID': self.client_id,
                'Authorization': 'Bearer {}'.format(response.json()['access_token'])}

    def _post(self, endpoint, query):
        url = self.main_url + endpoint
        response = requests.post(url,
                                 **query)

        # if access token has expired
        if response.status_code == 401:
            self.header = self._get_header()
            response = requests.post(url,
                                     **query)

        if not response.ok:
            raise HttpResponseServerError

        return response.json()

    def _compose_query_str(self, params=None):
        req = {'headers': self.header}

        if params and any(params.values()):
            req['data'] = ''
        else:
            return req

        for key, val in params.items():
            if not params[key]:
                continue
            else:
                req['data'] += key + ' '

            if key == 'fields' or key == 'exclude':
                req['data'] += ', '.join(map(str, val))
            elif key == 'where':
                req['data'] += ' & '.join(map(str, val))
            elif key == 'sort':
                req['data'] += ' '.join(map(str, val))
            else:
                req['data'] += str(val)

            req['data'] += ';'

        return req

    def _compose_query(self,
                       default_params=None,
                       enumeration_filters=None,
                       rating=None,
                       last_release_date=None,
                       count_of_games=None):
        params = {**default_params,
                  'where': [],
                  'sort': []}

        if enumeration_filters:
            for name, values in enumeration_filters.items():
                if not enumeration_filters[name]:
                    continue

                joined_values = ','.join(str(v) for v in values)
                params['where'].append(f'{name} = ({joined_values})')

        if last_release_date:
            params['where'].append('release_dates.date > '
                                   f'{int(last_release_date.timestamp())}')

        if rating:
            params['where'].append(f'rating >= {rating}')

        if count_of_games:
            params['limit'] = f'{count_of_games}'

        params['sort'].append('release_dates.date asc')

        return self._compose_query_str(params)

    @staticmethod
    def get_img_path(img_id):
        return 'https://images.igdb.com/igdb/' \
               f'image/upload/t_cover_big/{img_id}.jpg'

    def get_games(self,
                  genres=None,
                  platforms=None,
                  rating=None,
                  ids=None,
                  last_release_date=None,
                  count_of_games=None):
        enumeration_filters = {'genres': genres,
                               'platforms': platforms,
                               'id': ids}
        query = self._compose_query(default_params=self.default_params.copy(),
                                    enumeration_filters=enumeration_filters,
                                    rating=rating,
                                    last_release_date=last_release_date,
                                    count_of_games=count_of_games)
        games = self._post('games/', query)

        for game in games:
            if 'cover' in game:
                game['cover'] = self.get_img_path(game['cover']['image_id'])

            if last_release_date and 'release_dates' in game:
                game['release_dates'] = datetime.fromtimestamp(next(date['date'] for date
                                                                    in game['release_dates']
                                                                    if 'date' in date and
                                                                    date['date'] > int(last_release_date.timestamp())))
            elif 'release_dates' in game:
                game['release_dates'] = datetime.fromtimestamp(game['release_dates'][0]['date'])

            game['rating'] = game.get('rating', None)
            game['rating_count'] = game.get('rating_count', None)
            game['aggregated_rating'] = game.get('aggregated_rating', None)
            game['aggregated_rating_count'] = game.get('aggregated_rating_count', None)

            game['screenshots'] = [self.get_img_path(screenshot['image_id']) for screenshot in
                                   game['screenshots']] \
                if 'screenshots' in game else None
            game['platforms'] = [platform['name'] for platform
                                 in game['platforms']] \
                if 'platforms' in game else None
            game['genres'] = [genre['name'] for genre in game['genres']] \
                if 'genres' in game else None

        return games

    def get_game_by_id(self, game_id):
        games = self.get_games(ids=[game_id])

        if not games:
            raise LookupError('Game not found')

        return games[0]

    def get_platforms(self):
        return self._post('platforms/',
                          self._compose_query(default_params=self.default_params,
                                              enumeration_filters={'fields': 'name'}))

    def get_genres(self):
        return self._post('genres/',
                          self._compose_query(default_params=self.default_params,
                                              enumeration_filters={'fields': 'name'}))
