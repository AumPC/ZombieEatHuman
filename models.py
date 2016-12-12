import arcade.key
from random import randint, random
class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

class Ship(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        self.direction = Ship.DIR_VERTICAL


    def animate(self, delta):
            self.y += 5
            self.x += 5


class World:

    def __init__(self, width, height):
        self.width = width
        self.height = height
//        self.ship = Ship(self, 100, 100)
//        self.gold = Gold(self, 400, 400)


    def animate(self, delta):
        self.ship.animate(delta)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.ship.switch_direction()

class Gold(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

    def random_location(self):
        self.x = randint(0, self.world.width - 1)
        self.y = randint(0, self.world.height - 1)
