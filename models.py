import arcade.key
from random import randint, random

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)

class World:
##    NUM_ASTEROID = 20

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.zombie = Zombie(self,100, 100)
        self.human = Human(self, 400, 400,0,0,self.zombie)
        self.score = 0

        self.human.random_direction()
##        self.asteroids = []
##        for i in range(World.NUM_ASTEROID):
##            asteroid = Asteroid(self, 0, 0, 0, 0)
##            asteroid.random_direction()
##            self.asteroids.append(asteroid)
 
    def animate(self, delta):
        self.zombie.animate(delta)
        self.human.animate(delta)
        if self.zombie.hit(self.human, 15):
            self.human.random_location()
            self.score += 1
            self.human.random_direction()

            
##        for asteroid in self.asteroids:
##            asteroid.animate(delta)
##            if self.ship.hit(asteroid, 10):
##                self.score -= 1
##                asteroid.x = 0
##                asteroid.y = 0
##                asteroid.random_direction()

                
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.zombie.DIRECTION[0] = 1
        if key == arcade.key.RIGHT:
            self.zombie.DIRECTION[1] = 1
        if key == arcade.key.UP:
            self.zombie.DIRECTION[2] = 1
        if key == arcade.key.DOWN:
            self.zombie.DIRECTION[3] = 1

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.zombie.DIRECTION[0] = 0
        if key == arcade.key.RIGHT:
            self.zombie.DIRECTION[1] = 0
        if key == arcade.key.UP:
            self.zombie.DIRECTION[2] = 0
        if key == arcade.key.DOWN:
            self.zombie.DIRECTION[3] = 0


class Zombie(Model):
    DIRECTION = [0,0,0,0]  # LEFT RIGHT UP DOWN
    DIR_PIC = 1
    SPEED_X = 0
    SPEED_Y = 0
    xkeep = 650;
    def __init__(self, world, x, y):
        self.world = world
        super().__init__(world, x, y, 0)
        
    def walk(self):
        if self.DIRECTION[0] == 1: # LEFT
            self.DIR_PIC = 0
            self.SPEED_X = -5
        if self.DIRECTION[1] == 1: # RIGHT
            self.DIR_PIC = 1
            self.SPEED_X = 5
        if self.DIRECTION[2] == 1: # UP
            self.SPEED_Y = 5
        if self.DIRECTION[3] == 1: # DOWN
            self.SPEED_Y = -5
        if self.DIRECTION[0] == 0 and self.DIRECTION[1] == 0:
            self.SPEED_X = 0
        if self.DIRECTION[2] == 0 and self.DIRECTION[3] == 0:
            self.SPEED_Y = 0
            
    def animate(self, delta):
        self.walk()
        if self.y > self.world.height:
            self.y = 0
        if self.y < 0:
            self.y = self.world.height
        self.y += self.SPEED_Y
        if self.x > self.world.width:
            self.x = 0
        if self.x < 0:
            self.x = self.world.width
        self.x += self.SPEED_X
        self.xkeep = self.x

class Human(Model):
    def __init__(self, world, x, y,vx,vy,zombie):
        super().__init__(world, x, y, 0)
        self.vx = vx
        self.vy = vy
        self.zombie = zombie

    def random_direction(self):
        self.vx = 10 * random()
        self.vy = 10 * random()

    def random_location(self):
        self.x = randint(0, self.world.width - 1)
        self.y = randint(0, self.world.height - 1)

    def animate(self, delta):
##        if (self.x < 0) or (self.x > self.world.width):
##            self.vx = - self.vx
##        if (self.y < 0) or (self.y > self.world.height):
##            self.vy = - self.vy
        if self.y > self.world.height:
            self.y = 0
        if self.y < 0:
            self.y = self.world.height
        if self.x > self.world.width:
            self.x = 0
        if self.x < 0:
            self.x = self.world.width

        if (self.x > self.zombie.x-100) and (self.x < self.zombie.x) and (self.y > self.zombie.y-100) and (self.y < self.zombie.y+100):
            if self.vx > 0:
                self.vx = - self.vx
        elif (self.x > self.zombie.x) and (self.x < self.zombie.x+100) and (self.y > self.zombie.y-100) and (self.y < self.zombie.y+100):
            if self.vx < 0:
                self.vx = - self.vx
        if (self.x > self.zombie.x-100) and (self.x < self.zombie.x+100) and (self.y > self.zombie.y-100) and (self.y < self.zombie.y):
            if self.vy > 0:
                self.vy = - self.vy
        elif (self.x > self.zombie.x-100) and (self.x < self.zombie.x+100) and (self.y < self.zombie.y+100) and (self.y > self.zombie.y):
            if self.vy < 0:
                self.vy = - self.vy

        self.x += self.vx   
        self.y += self.vy


