from datetime import datetime


class Game:

    def __init__(self, name, description, release_date,
                 img_url, user_rating, user_rating_count,
                 critics_rating, critics_rating_count, must=False,
                 **kwargs):
        self.id = 1
        self.name = name
        self.img_url = img_url
        self.description = description
        self.release_date = release_date
        self.user_rating = user_rating
        self.user_rating_count = user_rating_count
        self.critics_rating = critics_rating
        self.critics_rating_count = critics_rating_count
        self.must = must
        self.genres = kwargs['genres']
        self.screenshots = kwargs['screenshots']
        self.platforms = kwargs['platforms']
        self.tweets = kwargs['tweets']


class Tweet:

    def __init__(self, content, date, user):
        self.content = content
        self.date = date
        self.user = user


class ModelManager:

    @staticmethod
    def get_temp_instance_of_game():
        tweets = [Tweet(
            'In 1999, Billy Mitchell of Hollywood, Florida became the first person to obtain a perfect score '
            'of 3,333,360 at Pac-Man, eating every possible dot, energizer, ghost, and bonus on every level '
            'without losing a single life in the process.',
            datetime.now(),
            'somebody')] * 3
