import arcade
import pathlib
import time
import random

WIDTH = 15 * 32
HEIGHT = 15 * 32

class TiledWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Tiled Map")
        self.mapLocation = pathlib.Path.cwd()/'Assets'/'map.tmx'
        self.mapList = None
        self.wallList = None
        self.enemy: arcade.AnimatedTimeBasedSprite = None
        self.enemy_list: arcade.SpriteList = None
        self.enemyMoveSpeed = 1.0
        self.displayTower1 = None
        self.displayTower2 = None
        self.displayTower3 = None
        self.displayTower4 = None
        self.displayTowerList = None
        self.tower1List = None
        self.tower2List = None
        self.tower3List = None
        self.tower4List = None
        self.start = 0.0

        self.townHealth = 10000
        self.currency = 300


    def setup(self):
        map = arcade.tilemap.read_tmx(str(self.mapLocation))
        self.mapList = arcade.tilemap.process_layer(map, 'traverse', 1)
        self.wallList = arcade.tilemap.process_layer(map, 'walls', 1)

        self.tower1List = arcade.SpriteList()
        self.tower2List = arcade.SpriteList()
        self.tower3List = arcade.SpriteList()
        self.tower4List = arcade.SpriteList()

        self.displayTowerList = arcade.SpriteList()

        self.displayTower1 = arcade.Sprite(pathlib.Path.cwd()/'Assets'/'tower1.png')
        self.displayTower2 = arcade.Sprite(pathlib.Path.cwd()/'Assets'/'towerTwo.png')
        self.displayTower3 = arcade.Sprite(pathlib.Path.cwd()/'Assets'/'tower3.png')
        self.displayTower4 = arcade.Sprite(pathlib.Path.cwd()/'Assets'/'tower4.png')

        self.displayTowerList.append(self.displayTower1)
        self.displayTowerList.append(self.displayTower2)
        self.displayTowerList.append(self.displayTower3)
        self.displayTowerList.append(self.displayTower4)

        y_pos = 3 * 32
        x_pos = 25
        count = 1
        for displayTower in self.displayTowerList:
            displayTower.center_y = y_pos
            displayTower.center_x = x_pos + 85 * count
            count += 1

        self.start = time.time()

        path = pathlib.Path.cwd() /'Assets'/ 'Archive' / 'walk'
        self.enemy = \
            arcade.AnimatedTimeSprite(0.5, center_x= WIDTH, center_y=  5 * 32)
        self.enemy_list = arcade.SpriteList()
        all_files = path.glob('*.png')
        textures = []
        for file_path in all_files:
            #print(file_path)
            frame = arcade.load_texture(str(file_path))  # we want the whole image
            textures.append(frame)
        print(textures)
        self.enemy.textures = textures
        self.enemy_list.append(self.enemy)


    def on_draw(self):
        arcade.start_render()
        self.mapList.draw()
        self.wallList.draw()
        self.enemy_list.draw()
        self.displayTowerList.draw()
        self.tower1List.draw()
        self.tower2List.draw()
        self.tower3List.draw()
        self.tower4List.draw()

        string = "Town Health: " + str(self.townHealth) + "; Currency earned: " + str(self.currency)
        arcade.draw_text("$100         $200             $400             $500", 25 * 4, 2 * 32, arcade.color.BLACK, 10)
        arcade.draw_text(" [A]              [S]              [D]                 [F]", 25 * 4, 1.5 * 32, arcade.color.BLACK, 10)
        arcade.draw_text(string, 25 * 3, 25, arcade.color.RED, 15)

    def on_key_press(self, key, modifiers):
        # Called everytime a key is pressed.

        if key == arcade.key.A:
            tower1 = arcade.Sprite(pathlib.Path.cwd()/'Assets'/'tower1.png')
            self.currentTower = tower1
            self.tower1List.append(tower1)
        elif key == arcade.key.S:
            tower2 = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'towerTwo.png')
            self.currentTower = tower2
            self.tower2List.append(tower2)
        elif key == arcade.key.D:
            tower3 = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'tower3.png')
            self.currentTower = tower3
            self.tower3List.append(tower3)
        elif key == arcade.key.F:
            tower4 = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'tower4.png')
            self.currentTower = tower4
            self.tower4List.append(tower4)

    def on_key_release(self, symbol: int, modifiers: int):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.currentTower.center_x = x
            self.currentTower.center_y = y

    def distance_between_sprites(self, sprite1: arcade.AnimatedTimeBasedSprite, sprite2: arcade.Sprite):
        x_diff = (sprite1.center_x - sprite2.center_x) ** 2
        y_diff = (sprite1.center_y - sprite2.center_y) ** 2
        return (x_diff + y_diff) ** (1/2)

    def update(self, delta_time: float):

        if len(arcade.check_for_collision_with_list(self.enemy, self.wallList)) == 0:
            self.enemy.center_x = self.enemy.center_x - self.enemyMoveSpeed
            print("enemy collided!")
        else:
            self.enemy.center_x = self.enemy.center_x + 0

        if (time.time() - self.start >= 1.0):
            self.start = time.time()
            y_position = random.randint(5 * 32, HEIGHT)
            path = pathlib.Path.cwd() / 'Assets' / 'Archive' / 'walk'
            enemy : arcade.AnimatedTimeBasedSprite = \
                arcade.AnimatedTimeSprite(0.5, center_x=WIDTH, center_y= y_position)
            #enemy.center_x = enemy.center_x - 0.5
            all_files = path.glob('*.png')
            textures = []
            for file_path in all_files:
                #print(file_path)
                frame = arcade.load_texture(str(file_path))  # we want the whole image
                textures.append(frame)
            enemy.textures = textures
            #enemy.center_x = enemy.center_x - 0.5
            self.enemy_list.append(enemy)


        if len(self.tower1List) != 0:
            if len(self.enemy_list) >= len(self.tower1List):
                for enemy in self.enemy_list:
                    for tower in self.tower1List:
                        if self.distance_between_sprites(enemy, tower) <= 50.0:
                            enemy.change_x = 0.2

            elif len(self.enemy_list) < len(self.tower1List):
                for tower in self.tower1List:
                    for enemy in self.enemy_list:
                        if self.distance_between_sprites(enemy, tower) <= 50.0:
                            enemy.center_x = enemy.center_x + 1.0

        for enemy in self.enemy_list:
            enemy.update_animation()
            if len(arcade.check_for_collision_with_list(enemy, self.wallList)) == 0:
                enemy.center_x = enemy.center_x - self.enemyMoveSpeed
            else:
                enemy.center_x = enemy.center_x + 0

        self.enemy_list.update()





def main():
    window: TiledWindow = TiledWindow()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
