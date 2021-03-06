import arcade
from models import Zombie,World,Human,Bullet

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        self.angle = self.model.angle
        super().draw()

 
class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.state = 3
        self.highscore = 0
        self.set_game(width, height)
        
    def set_game(self,width, height):
        self.world = World(width,height)
        self.zombie_sprite = ModelSprite('images/zombie.png',model=self.world.zombie)
        self.human_sprites = []
        self.bullet_sprites = []
        for human in self.world.human:
            self.human_sprites.append(ModelSprite('images/human.png',model=human))
        for bullet in self.world.bullet:
            self.bullet_sprites.append(ModelSprite('images/bullet.png',model=bullet))

    def on_draw(self):
        arcade.start_render()
        if self.state == 1:
            texture = arcade.load_texture('images/background_start.png')
            arcade.draw_texture_rectangle(self.width/2, self.height/2,
                                      texture.width, texture.height, texture, 0)
        if self.state == 2:
            self.draw_bar()
            self.time_change()
            for b in self.bullet_sprites:
                b.draw()
            for i in range(self.world.NUM_HUMAN):
                if self.world.human_speedX[i] > 0:
                    self.human_sprites[i] = ModelSprite('images/human.png',model=self.world.human[i])
                else:
                    self.human_sprites[i] = ModelSprite('images/human1.png',model=self.world.human[i])
                self.human_sprites[i].draw()
            if self.world.DIR_PIC == 0: 
                self.zombie_sprite = ModelSprite('images/zombie.png',model=self.world.zombie)
            elif self.world.DIR_PIC == 1: 
                self.zombie_sprite = ModelSprite('images/zombie1.png',model=self.world.zombie)
            self.zombie_sprite.draw()
        if self.state == 3:
            texture = arcade.load_texture('images/background_ending.png')
            arcade.draw_texture_rectangle(self.width/2, self.height/2,
                                      texture.width, texture.height, texture, 0)
            arcade.draw_text("     SCORE : " + str(self.world.score),
                         self.width/2-50, self.height - 50,
                         arcade.color.PINK, 20)
            if self.highscore < self.world.score:
                self.highscore = self.world.score
            arcade.draw_text("HIGHSCORE : " + str(self.highscore),
                         self.width/2-50, self.height - 80,
                         arcade.color.PINK, 20)
  
    def animate(self, delta):
        if self.state == 2:
            self.world.animate(delta)
        if self.world.live <= 0:
            self.state = 3

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
        if self.state == 1:
            if key == arcade.key.ENTER:
                self.set_game(self.width, self.height)
                self.state = 2
        if self.state == 3:
            if key == arcade.key.ENTER:
                self.set_game(self.width, self.height)
                self.state = 2
        
    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def draw_bar(self):
        texture = arcade.load_texture('images/background.jpg')
        arcade.draw_texture_rectangle(self.width/2, self.height/2,
                                      texture.width, texture.height, texture, 0)
        arcade.draw_rectangle_filled(self.width/2, self.height-22.5,
                                     SCREEN_WIDTH , 45, arcade.color.BLACK)
        texture = arcade.load_texture('images/heart.png')
        arcade.draw_text("LIVE : ",
                         self.width/2 - 85, self.height - 30,
                         arcade.color.WHITE, 20)
        for m in range(self.world.live):
            arcade.draw_texture_rectangle(self.width/2 + m*40, self.height - 22.5,
                                      texture.width, texture.height, texture, 0)
        minutes = int(self.world.total_time) // 60
        seconds = int(self.world.total_time) % 60
        output = "TIME : {:02d}:{:02d}".format(minutes, seconds)
        arcade.draw_text(output, 10, self.height - 30, arcade.color.WHITE, 20)
        arcade.draw_text("SCORE : " + str(self.world.score),
                         self.width - 140, self.height - 30,
                         arcade.color.WHITE, 20)

    def time_change(self):
        if (int(self.world.total_time)-self.world.delta_time_spawn) >= 59:
            for i in range(5):
                self.human_sprites.append(ModelSprite('images/human.png',model=self.world.human[i]))
                self.bullet_sprites.append(ModelSprite('images/bullet.png',model=self.world.human[i]))

if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()

