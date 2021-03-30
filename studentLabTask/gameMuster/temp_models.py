

class Game:

    def __init__(self, name, img_url, *genres):
        self.name = name
        self.img_url = img_url
        self.genres = ' '.join(genres)