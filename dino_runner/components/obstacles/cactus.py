import random
from .obstacle import Obstacle

class Cactus(Obstacle):
    def __init__(self, images):
        self.type = random.randint(0, 5)
        super().__init__(images, self.type)
        if self.type == 0 or self.type == 1 or self.type == 2:
            self.rect.y = 295
        elif self.type == 3 or self.type == 4 or self.type == 5:
            self.rect.y = 320

