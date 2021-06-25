"""View additional functions tests"""
from django.http.request import QueryDict, MultiValueDict

from gameMuster.tests.base_test import BaseTest
from gameMuster import views


class ViewAdditionalFuncsTest(BaseTest):
    """View additional functions tests"""

    def test_get_list_of_filters(self):
        """Test data from filter fields to convert to the list of integers"""
        data_from_filter = {
            "genres": list(map(str, self.faker.pylist(value_types=int)))
        }
        filter_query_dict = QueryDict("", mutable=True)
        filter_query_dict.update(MultiValueDict(data_from_filter))

        genre_ids = views.get_list_of_filters("genres", filter_query_dict)

        for genre_id in genre_ids:
            self.assertIsInstance(genre_id, int)

        self.assertCountEqual(list(map(int, data_from_filter["genres"])), genre_ids)

    def test_get_game_genres(self):
        """Test genres grouped by game id"""
        genres = views.get_game_genres([self.game])
        genre_name = genres[self.game.id][0]

        self.assertEquals(genre_name, self.genre.name)
