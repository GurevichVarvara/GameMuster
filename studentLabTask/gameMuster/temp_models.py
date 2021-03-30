

class Game:

    def __init__(self, name, description, release_date,
                 img_url, user_rating, user_rating_count,
                 critics_rating, critics_rating_count,
                 **kwargs):
        self.name = name
        self.img_url = img_url
        self.description = description
        self.release_date = release_date
        self.user_rating = user_rating
        self.user_rating_count = user_rating_count
        self.critics_rating = critics_rating
        self.critics_rating_count = critics_rating_count
        self.genres = ' '.join(kwargs['genres'])
        self.screenshots = kwargs['screenshots']
        self.platforms = kwargs['platforms']
        self.tweets = kwargs['tweets']


class Tweet:

    def __init__(self, content, date, user):
        self.content = content
        self.date = date
        self.user = user
