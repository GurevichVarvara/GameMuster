import requests
from gameMuster.temp_models import Game

IGDB_CLIENT_ID = 'gf9n0dlg05nzp9uecs4dtrwyqob4f2'
IGDB_CLIENT_SECRET = 'lyiongrvu9cj696o62t281sgcndwfa'


class GamesManager:

    def __init__(self):
        self.igdb_main_url = 'https://api.igdb.com/v4/'
        self.header = self.get_access_token()
        print(self.header)

    @staticmethod
    def get_access_token():
        access_token = requests.post('https://id.twitch.tv/oauth2/'
                                     'token?client_id={}&client_secret'
                                     '={}&grant_type=client_credentials'.format(
                                        IGDB_CLIENT_ID,
                                        IGDB_CLIENT_SECRET)).json()['access_token']

        return {'Client-ID': IGDB_CLIENT_ID,
                'Authorization': 'Bearer {}'.format(access_token)}

    def check_access_token_status(self, response_from_igdb):
        if response_from_igdb.get('message', None) == "Authorization Failure. Have you tried:":
            self.header = GamesManager.get_access_token()

    def generate_games(self):
        params = {'fields': 'id, name, cover, summary,'
                            'created_at, aggregated_rating,'
                            'rating_count, genres, screenshots, '
                            'platforms'}
        result_games = requests.post(self.igdb_main_url + 'games/',
                                     headers=self.header,
                                     params=params).json()[0]
        print(result_games)




