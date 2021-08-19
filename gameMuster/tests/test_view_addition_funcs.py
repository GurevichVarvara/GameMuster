"""View additional functions tests"""
import pickle

from django.http.request import QueryDict, MultiValueDict

from gameMuster.tests.base_test import BaseTest
from gameMuster import views
from gameMuster.models import Genre
from gameMuster.game_managers.games_manager import games_manager


class ViewAdditionalFuncsTest(BaseTest):
    """View additional functions tests"""

    def test_get_list_of_filters(self):
        """Test data from filter fields to convert to the list of integers"""
        data_from_filter = {"genres": ["1", "2"]}
        filter_query_dict = QueryDict("", mutable=True)
        filter_query_dict.update(MultiValueDict(data_from_filter))

        genre_ids = views.get_list_of_filters("genres", filter_query_dict)

    def test_get_game_genres(self):
        """Test genres grouped by game id"""
        genres = views.get_game_genres([self.game])
        genre_name = genres[self.game.id][0]

        self.assertEquals(genre_name, self.genre.name)
