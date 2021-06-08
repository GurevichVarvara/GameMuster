"""IGBD API tests"""

from django.conf import settings

from gameMuster.tests.base_test import BaseTest
from gameMuster.api_wrappers.igdb_wrapper import IgdbWrapper


class IgdbWrapperTestCase(BaseTest):
    """IGBD API tests"""
    igdb_wrapper = IgdbWrapper(settings.IGDB_CLIENT_ID,
                               settings.IGDB_CLIENT_SECRET)

    def test_get_header(self):
        """Test that igdb wrapper returns right fields in header"""
        header = self.igdb_wrapper._get_header()

        self.assertIn('Client-ID', header)
        self.assertIn('Authorization', header)

    def test_compose_query_str(self):
        """Test that wrapper make right query string from query params"""
        query_str = self.igdb_wrapper._compose_query_str(
            {'fields': ['id', 'name'],
             'exclude': ['surname'],
             'where': ['name = (var)',
                       'id > 4'],
             'sort': ['release_dates.date asc'],
             'limit': '5'})

        self.assertIn('data', query_str)
        self.assertEquals(query_str['data'],
                          'fields id, name;'
                          'exclude surname;'
                          'where name = (var) & id > 4;'
                          'sort release_dates.date asc;'
                          'limit 5;')

    def test_compose_query(self):
        """Test that wrapper make right query string from dict with filters"""
        query_str = self.igdb_wrapper._compose_query(
            enumeration_filters={'genres': [1, 2],
                                 'platforms': [1, 2]},
            rating=50,
            count_of_games=10)

        self.assertIn('data', query_str)
        self.assertEquals(query_str['data'],
                          'where genres = (1,2) & '
                          'platforms = (1,2) & '
                          'rating >= 50;'
                          'sort release_dates.date asc;'
                          'limit 10;')

    def test_get_img_path(self):
        """Test that method returns right image path"""
        img_path = IgdbWrapper.get_img_path('1')

        self.assertEquals(img_path,
                          'https://images.igdb.com/igdb/image/'
                          'upload/t_cover_big/1.jpg')

    def test_get_games(self):
        """Test that method returns games with proper fields"""
        games = self.igdb_wrapper.get_games()
        required_fields = [field.split('.', 1)[0] for field
                           in self.igdb_wrapper.default_params['fields']]

        self.check_list(games, dict)
        for required_field in required_fields:
            self.assertIn(required_field, games[0])

    def test_get_game_by_id(self):
        """Test that method returns game with proper id"""
        game = self.igdb_wrapper.get_game_by_id(1)

        self.assertIsInstance(game, dict)
        self.assertEquals(game['id'], 1)

    def test_get_platforms(self):
        """Test that method returns platforms with proper fields"""
        platforms = self.igdb_wrapper.get_platforms()

        self.check_list(platforms, dict)
        self.assertIn('name', platforms[0])

    def test_get_genres(self):
        """Test that method returns genres with proper fields"""
        genres = self.igdb_wrapper.get_genres()

        self.check_list(genres, dict)
        self.assertIn('name', genres[0])