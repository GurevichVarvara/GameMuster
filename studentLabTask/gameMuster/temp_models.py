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
            'somebody',
            datetime.now())] * 3

        game = Game('PACKMAN',
                    'Pac-Man is a maze chase video game; the player controls the eponymous character through an '
                    'enclosed maze. The objective of the game is to eat all of the dots placed in the maze while '
                    'avoiding four colored ghosts — Blinky (red), Pinky (pink), Inky (cyan), and Clyde (orange) — '
                    'that pursue him. When all of the dots are eaten, the player advances to the next level. If '
                    'Pac-Man makes contact with a ghost, he will lose a life; the game ends when all lives are '
                    'lost. Each of the four ghosts have their own unique, distinct artificial intelligence (A.I.), '
                    'or "personalities"; Blinky gives direct chase to Pac-Man, Pinky and Inky try to position '
                    'themselves in front of Pac-Man, usually by cornering him, and Clyde will switch between '
                    'chasing Pac-Man and fleeing from him ',
                    datetime.now(),
                    'https://i1.sndcdn.com/avatars-000527330727-10g55j-t240x240.jpg',
                    7.8,
                    123,
                    4.0,
                    123,
                    True,
                    genres=['Arcade', 'Oldschool'],
                    screenshots=['https://99px.ru/sstorage/53/2012/03/tmb_36321_9414.jpg',
                                 'https://st3.depositphotos.com/1635692/16714/v/600/depos'
                                 'itphotos_167140316-stock-illustration-pac-man-traffic-jam.jpg'],
                    platforms=['PC', 'PS4'],
                    tweets=tweets)

        return game
