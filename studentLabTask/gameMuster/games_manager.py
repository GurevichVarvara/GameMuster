import requests

IGDB_CLIENT_ID = 'gf9n0dlg05nzp9uecs4dtrwyqob4f2'
IGDB_CLIENT_SECRET = 'lyiongrvu9cj696o62t281sgcndwfa'


class GamesManager:

    def __init__(self):
        self.igdb_main_url = 'https://api.igdb.com/v4/'
        self.access_token = self.get_access_token()

        print(self.access_token)

    @staticmethod
    def get_access_token():

        access_token = requests.post('https://id.twitch.tv/oauth2/'
                                    'token?client_id={}&client_secret'
                                    '={}&grant_type=client_credentials'.format(
                                        IGDB_CLIENT_ID,
                                        IGDB_CLIENT_SECRET)).json()['access_token']

        return {'Client-ID': IGDB_CLIENT_ID,
                'Authorization': 'Bearer {}'.format(access_token)}


