

class Game:

    def __init__(self, game_id, name,
                 img_url, genres, description,
                 release_date, user_rating,
                 user_rating_count, critics_rating,
                 critics_rating_count, must=False,
                 **kwargs):
        self.game_id = game_id
        self.name = name
        self.img_url = img_url
        self.genres = genres
        self.must = must
        self.description = description
        self.release_date = release_date
        self.user_rating = user_rating
        self.user_rating_count = user_rating_count
        self.critics_rating = critics_rating
        self.critics_rating_count = critics_rating_count
        self.screenshots = kwargs['screenshots']
        self.platforms = kwargs['platforms']
        self.tweets = kwargs['tweets']


class Tweet:

    def __init__(self, content, date, user):
        self.content = content
        self.date = date
        self.user = user
