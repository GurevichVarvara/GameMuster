import requests
from gameMuster.temp_models import Game

IGDB_CLIENT_ID = 'gf9n0dlg05nzp9uecs4dtrwyqob4f2'
IGDB_CLIENT_SECRET = 'o38ky7c3iqhk4l6b1f35hayaca8ii9'


class GamesManager:

    def __init__(self):
        self.igdb_main_url = 'https://api.igdb.com/v4/'
        self.igdb_header = self.get_access_igdb_token()
        print(self.igdb_header)

    @staticmethod
    def get_access_igdb_token():
        access_token = requests.post('https://id.twitch.tv/oauth2/'
                                     'token?client_id={}&client_secret'
                                     '={}&grant_type=client_credentials'.format(
                                        IGDB_CLIENT_ID,
                                        IGDB_CLIENT_SECRET)).json()['access_token']

        return {'Client-ID': IGDB_CLIENT_ID,
                'Authorization': 'Bearer {}'.format(access_token)}

    def get_api_response(self, access_token_func, url, headers, params):
        response_from_api = requests.post(url, headers=headers, params=params)

        # if access token has expired
        if response_from_api.status_code != 200:
            self.igdb_header = access_token_func()
            response_from_api = requests.post(url, headers=headers, params=params)

        return response_from_api.json()[0]

    def generate_games(self):
        params = {'fields': 'id, name, cover, summary,'
                            'created_at, aggregated_rating,'
                            'rating_count, genres, screenshots, '
                            'platforms'}

        result_games = self.get_api_response(self.get_access_igdb_token,
                                             self.igdb_main_url + 'games/',
                                             self.igdb_header,
                                             params)
        print(result_games)




