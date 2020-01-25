import arcade
import pathlib
import time
import random
import math

WIDTH = 15 * 32
HEIGHT = 15 * 32

class TiledWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Tiled Map")
        self.mapLocation = pathlib.Path.cwd()/'Assets'/'map.tmx'
        self.mapLocation2 = pathlib.Path.cwd()/'Assets'/'map2.tmx'
        self.mapLocation3 = pathlib.Path.cwd() / 'Assets' / 'map3.tmx'
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
        self.bulletList = None
        self.bulletList2 = None
        self.start = 0.0
        self.frame = 0
        self.townHealth = 1000
        self.currency = 500
        self.enemiesKilled = 0
        self.tower3Damage = 25
        self.tower4Damage = 25
        self.isGameOver = False
        path = pathlib.Path.cwd()/'Assets'/'magnum.wav'
        #self.magnumShot = arcade.sound.load_sound('/Users/apple/Desktop/TheGame/Assets/magnum.wav')
        self.magnumShot = arcade.sound.load_sound(str(path))
        #self.nineShot = arcade.sound.load_sound(pathlib.Path.cwd() / 'Assets' / 'nine.wav')
        path2 = pathlib.Path.cwd()/'Assets'/'shotgun_blast.wav'
        #self.shotGunShot = arcade.sound.load_sound('/Users/apple/Desktop/TheGame/Assets/shotgun_blast.wav')
        self.shotGunShot = arcade.sound.load_sound(str(path2))

    def setup(self):
        map = arcade.tilemap.read_tmx(str(self.mapLocation))
        self.mapList = arcade.tilemap.process_layer(map, 'traverse', 1)
        self.wallList = arcade.tilemap.process_layer(map, 'walls', 1)

        self.tower1List = arcade.SpriteList()
        self.tower2List = arcade.SpriteList()
        self.tower3List = arcade.SpriteList()
        self.tower4List = arcade.SpriteList()

        self.bulletList = arcade.SpriteList()
        self.bulletList2 = arcade.SpriteList()

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
        self.bulletList.draw()
        self.bulletList2.draw()



        if self.isGameOver == True and self.enemiesKilled < 60:
            string1 = "YOU LOST! Score: " + str(self.enemiesKilled)
            print("Game Over")
            arcade.draw_text(string1, WIDTH // 2 - 100, HEIGHT // 2, arcade.color.BLACK, 20)

        elif self.isGameOver == True and self.enemiesKilled >= 60:
            string = "You WON! Score: " + str(self.enemiesKilled)
            print("Game Over")
            arcade.draw_text(string, WIDTH // 2 - 100, HEIGHT // 2, arcade.color.BLACK, 20)


        string = "Town Health: " + str(self.townHealth) + "; Currency earned: $" + str(self.currency) + "; Enemies killed: " + str(self.enemiesKilled)
        arcade.draw_text("$100         $150             $300             $500", 25 * 4, 2 * 32, arcade.color.BLACK, 10)
        arcade.draw_text(" [A]              [S]              [D]                 [F]", 25 * 4, 1.5 * 32, arcade.color.BLACK, 10)
        arcade.draw_text(string, 25 * 2, 25, arcade.color.RED, 12)

    def on_key_press(self, key, modifiers):
        # Called everytime a key is pressed.

        if key == arcade.key.A and self.currency >= 100:
            tower1 = arcade.Sprite(pathlib.Path.cwd()/'Assets'/'tower1.png')
            self.currentTower = tower1
            self.tower1List.append(tower1)
            self.currency -= 100
        elif key == arcade.key.S and self.currency >= 150:
            tower2 = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'towerTwo.png')
            self.currentTower = tower2
            self.tower2List.append(tower2)
            self.currency -= 150
        elif key == arcade.key.D and self.currency >= 300:
            tower3 = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'tower3.png')
            self.currentTower = tower3
            self.tower3List.append(tower3)
            self.currency -= 300
        elif key == arcade.key.F and self.currency >= 500:
            tower4 = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'tower4.png')
            self.currentTower = tower4
            self.tower4List.append(tower4)
            self.currency -= 500

    def on_key_release(self, symbol: int, modifiers: int):
        self.currentTower = None

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.currentTower.center_x = x
            self.currentTower.center_y = y

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        self.currentTower = None

    def distance_between_sprites(self, sprite1: arcade.AnimatedTimeBasedSprite, sprite2: arcade.Sprite):
        x_diff = (sprite1.center_x - sprite2.center_x) ** 2
        y_diff = (sprite1.center_y - sprite2.center_y) ** 2
        return (x_diff + y_diff) ** (1/2)

    def update(self, delta_time: float):

        self.frame += 1


        if self.isGameOver:
            time.sleep(10)
            arcade.close_window()

        if len(arcade.check_for_collision_with_list(self.enemy, self.wallList)) == 0:
            self.enemy.center_x = self.enemy.center_x - self.enemyMoveSpeed
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
                            enemy.change_x = 0.2


        if len(self.tower2List) != 0:
            if len(self.enemy_list) >= len(self.tower2List):
                for enemy in self.enemy_list:
                    for tower in self.tower2List:
                        if self.distance_between_sprites(enemy, tower) <= 32.0:
                            enemy.kill()
                            self.enemiesKilled += 1
                            self.currency += 50

            elif len(self.enemy_list) < len(self.tower2List):
                for tower in self.tower2List:
                    for enemy in self.enemy_list:
                        if self.distance_between_sprites(enemy, tower) <= 32.0:
                            enemy.kill()
                            self.enemiesKilled += 1
                            self.currency += 50

        if len(self.tower3List) != 0:

            if len(self.enemy_list) >= len(self.tower3List):
                for enemy in self.enemy_list:
                    for tower in self.tower3List:
                        if self.distance_between_sprites(enemy, tower) <= 50.0:
                            x = enemy.center_x - tower.center_x
                            y = enemy.center_y - tower.center_y
                            angle = math.atan2(y, x)
                            tower.angle = math.degrees(angle) - 90
                            if self.frame % 60 == 0 and self.checkBounds(enemy):
                                bullet = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'bullet.png')
                                bullet.center_x = tower.center_x
                                bullet.center_y = tower.center_y
                                bullet.angle = math.degrees(angle)
                                bullet.change_x = math.cos(angle) * 10
                                bullet.change_y = math.sin(angle) * 10
                                self.bulletList.append(bullet)
                                arcade.play_sound(self.magnumShot)
            elif len(self.enemy_list) < len(self.tower3List):
                for tower in self.tower3List:
                    for enemy in self.enemy_list:
                        if self.distance_between_sprites(enemy, tower) <= 50.0:
                            x = enemy.center_x - tower.center_x
                            y = enemy.center_y - tower.center_y
                            angle = math.atan2(y, x)
                            tower.angle = math.degrees(angle) - 90
                            if self.frame % 60 == 0 and self.checkBounds(enemy):
                                bullet = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'bullet.png')
                                bullet.center_x = tower.center_x
                                bullet.center_y = tower.center_y
                                bullet.angle = math.degrees(angle)
                                bullet.change_x = math.cos(angle) * 10
                                bullet.change_y = math.sin(angle) * 10
                                self.bulletList.append(bullet)
                                arcade.play_sound(self.magnumShot)

        if len(self.tower4List) != 0:

            if len(self.enemy_list) >= len(self.tower4List):
                for enemy in self.enemy_list:
                    for tower in self.tower4List:
                        if self.distance_between_sprites(enemy, tower) <= 70.0:
                            x = enemy.center_x - tower.center_x
                            y = enemy.center_y - tower.center_y
                            angle = math.atan2(y, x)
                            tower.angle = math.degrees(angle) - 90
                            if self.frame % 30 == 0 and self.checkBounds(enemy):
                                bullet = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'bullet.png')
                                bullet.center_x = tower.center_x
                                bullet.center_y = tower.center_y
                                bullet.angle = math.degrees(angle)
                                bullet.change_x = math.cos(angle) * 20
                                bullet.change_y = math.sin(angle) * 20
                                self.bulletList2.append(bullet)
                                arcade.play_sound(self.shotGunShot)
            elif len(self.enemy_list) < len(self.tower4List):
                for tower in self.tower4List:
                    for enemy in self.enemy_list:
                        if self.distance_between_sprites(enemy, tower) <= 70.0:
                            x = enemy.center_x - tower.center_x
                            y = enemy.center_y - tower.center_y
                            angle = math.atan2(y, x)
                            tower.angle = math.degrees(angle) - 90
                            if self.frame % 30 == 0 and self.checkBounds(enemy):
                                bullet = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'bullet.png')
                                bullet.center_x = tower.center_x
                                bullet.center_y = tower.center_y
                                bullet.angle = math.degrees(angle)
                                bullet.change_x = math.cos(angle) * 20
                                bullet.change_y = math.sin(angle) * 20
                                self.bulletList2.append(bullet)
                                arcade.play_sound(self.shotGunShot)

        for bullet in self.bulletList:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        for bullet2 in self.bulletList2:
            if bullet2.top < 0:
                bullet2.remove_from_sprite_lists()

        self.bulletList.update()
        self.bulletList2.update()


        for enemy in self.enemy_list:
            enemyHealth: int = 25
            enemy.update_animation()
            if len(arcade.check_for_collision_with_list(enemy, self.wallList)) == 0:
                enemy.center_x = enemy.center_x - self.enemyMoveSpeed
            else:
                enemy.center_x = enemy.center_x + 0

            if enemy.center_x <= 0:
                self.townHealth -= 50
                enemy.kill()
                continue

            enemyGetsHit = arcade.check_for_collision_with_list(enemy, self.bulletList)
            enemyGetsHit2 = arcade.check_for_collision_with_list(enemy, self.bulletList2)
            if enemyGetsHit:
                enemyHealth = enemyHealth - self.tower3Damage
                if enemyHealth <= 0:

                    enemy.kill()
                    self.enemiesKilled += 1
                    self.currency += 30
                    for bullet in enemyGetsHit:
                        if bullet.center_x == enemy.center_x and bullet.center_y == enemy.center_y:
                            bullet.kill()

            if enemyGetsHit2:
                enemyHealth = enemyHealth - self.tower4Damage
                if enemyHealth <= 0:

                    enemy.kill()
                    self.enemiesKilled += 1
                    self.currency += 20
                    for bullet2 in enemyGetsHit2:
                        if bullet2.center_x == enemy.center_x and bullet2.center_y == enemy.center_y:
                            bullet2.kill()

        if self.townHealth <= 0:
            self.isGameOver = True

        if self.enemiesKilled >= 10:
            mapLayer = arcade.tilemap.read_tmx(str(self.mapLocation2))
            self.mapList = arcade.tilemap.process_layer(mapLayer, 'traverse', 1)
            self.wallList = arcade.tilemap.process_layer(mapLayer, 'walls', 1)

        if self.enemiesKilled >= 20:
            mapLayer = arcade.tilemap.read_tmx(str(self.mapLocation3))
            self.mapList = arcade.tilemap.process_layer(mapLayer, 'traverse', 1)
            self.wallList = arcade.tilemap.process_layer(mapLayer, 'walls', 1)

        if self.enemiesKilled >= 60:
            self.isGameOver = True

        self.bulletList.update()

        self.enemy_list.update()

    def checkBounds(self, sprite: arcade.AnimatedTimeBasedSprite):
        if sprite.center_x >= 32 and sprite.center_y >= 32 and sprite.center_x <= 448 and sprite.center_y <= 478:
            return True
        else:
            return False


def main():
    window: TiledWindow = TiledWindow()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()