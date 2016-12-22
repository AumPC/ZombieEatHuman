import arcade.key
from math import atan2 , degrees,sin,cos
from random import randint, uniform

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)


class World:
    def __init__(self, width, height):
        self.NUM_HUMAN = 20
        self.width = width
        self.height = height
        self.zombie = Zombie(self,100, 100)
        self.human = []
        self.bullet = []
        self.human_speedX = []
        for i in range(self.NUM_HUMAN):
            human = Human(self, randint(self.width/2, self.width - 1), randint(self.height/2, self.height - 46),0,0,self.zombie)
            human.random_direction()
            self.human.append(human)
            self.human_speedX.append(self.human[i].vx)
            bullet = Bullet(self, self.human[i].x, self.human[i].y,self.zombie)
            self.bullet.append(bullet)
        self.DIR_PIC = 1
        self.score = 0
        self.total_time = 0
        self.live = 5
        self.delta_time = int(self.total_time)
        self.delta_time_spawn = int(self.total_time)
 
    def animate(self, delta):
        self.total_time += delta
        self.time_change()
        self.zombie.animate(delta)
        for i in range(self.NUM_HUMAN):
            self.human[i].animate(delta)
            self.human_speedX[i] = self.human[i].vx
            if self.zombie.hit(self.human[i], 20):
                self.human[i].random_location()
                self.score += 1
                self.human[i].random_direction()
            self.bullet[i].animate(delta)
            if self.zombie.hit(self.bullet[i], 15) and self. bullet[i].alive == 1:
                self.bullet[i].alive = 0
                self.live -= 1
                self.bullet[i].time_back = 10
            if self.bullet[i].alive == 0 and self.bullet[i].time_back <= 0 :
                self.bullet[i].shoot(self.human[i].x, self.human[i].y)
                
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.zombie.DIRECTION[0] = 1
            self.DIR_PIC = 0
        if key == arcade.key.RIGHT:
            self.zombie.DIRECTION[1] = 1
            self.DIR_PIC = 1
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

    def time_change(self):
        if (int(self.total_time)-self.delta_time) >= 15:
            self.live += 1
            self.delta_time = int(self.total_time)
        if (int(self.total_time)-self.delta_time_spawn) >= 60:
            self.delta_time_spawn = int(self.total_time)
            for i in range(5):
                human = Human(self, randint(self.width/2, self.width - 1), randint(self.height/2, self.height - 46),0,0,self.zombie)
                human.random_direction()
                self.human.append(human)
                self.human_speedX.append(self.human[i].vx)
                bullet = Bullet(self, self.human[i].x, self.human[i].y,self.zombie)
                self.bullet.append(bullet)
            self.NUM_HUMAN += 5


class Zombie(Model):
    DIRECTION = [0,0,0,0]  # LEFT RIGHT UP DOWN
    SPEED_X = 0
    SPEED_Y = 0
    SPEED = 8
    def __init__(self, world, x, y):
        self.world = world
        super().__init__(world, x, y, 0)
        self.DIR_PIC = 1    
        
    def walk(self):
        if self.DIRECTION[0] == 1: # LEFT
            self.SPEED_X = -self.SPEED
        if self.DIRECTION[1] == 1: # RIGHT
            self.SPEED_X = self.SPEED
        if self.DIRECTION[2] == 1: # UP
            self.SPEED_Y = self.SPEED
        if self.DIRECTION[3] == 1: # DOWN
            self.SPEED_Y = -self.SPEED
        if self.DIRECTION[0] == 0 and self.DIRECTION[1] == 0:
            self.SPEED_X = 0
        if self.DIRECTION[2] == 0 and self.DIRECTION[3] == 0:
            self.SPEED_Y = 0
            
    def animate(self, delta):
        self.walk()
        if self.y > self.world.height-50:
            self.y = 0
        if self.y < 0:
            self.y = self.world.height-50
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
        self.vx = 3*uniform(-1,1)
        self.vy = 3*uniform(-1,1)
        if self.vx > 0:
            self.vx += 3
        if self.vx < 0:
            self.vx -= 3
        if self.vy > 0:
            self.vy += 3
        if self.vy < 0:
            self.vy -= 3
                
    def random_location(self):
        self.x = randint(0, self.world.width - 1)
        self.y = randint(0, self.world.height - 1)

    def animate(self, delta):
        self.border()
        self.near_zombie()
        self.x += self.vx   
        self.y += self.vy

    def border(self):
        if self.y > self.world.height-50:
            self.y = 0
        if self.y < 0:
            self.y = self.world.height-50
        if self.x > self.world.width:
            self.x = 0
        if self.x < 0:
            self.x = self.world.width

    def near_zombie(self):
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

                
class Bullet(Model):
    SPEED = 4
    def __init__(self, world, x, y,zombie):
        super().__init__(world, x, y, 0)
        self.zombie = zombie
        self.shoot(x,y)

    def animate(self, delta):
        if (int(self.world.total_time)-self.world.delta_time_spawn)%30 == 0 and self.SPEED <= 6:
            self.SPEED += 1
        self.x += self.vx   
        self.y += self.vy
        if (self.time_back < 0) and ((self.x > self.world.width) or (self.x < 0) or (self.y > self.world.height-50) or (self.y < 0)):
            self.alive = 0
            self.time_back = 10
        self.time_back -= 1

    def shoot(self,human_x,human_y):
        self.alive = 1
        self.time_back = 0
        self.x = human_x
        self.y = human_y
        self.angle = 180 + degrees(atan2((self.zombie.y-self.y),(self.zombie.x-self.x)))
        if self.x >= self.zombie.x:
            self.vx = -self.SPEED
        if self.x < self.zombie.x:
            self.vx = self.SPEED
        if self.y >= self.zombie.y:
            self.vy = -self.SPEED
        if self.y < self.zombie.y:
            self.vy = self.SPEED
