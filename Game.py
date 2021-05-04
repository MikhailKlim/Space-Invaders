import pygame
import game_object
from level import *
from game_menu import *
from constants import *
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()


class Game:
    def __init__(self):
        pygame.init()
        self.levels = Level()
        self.screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        pygame.display.set_caption('Space Invaders')
        self.pl_last_x = 0
        self.pl_last_y = 0
        self.player = game_object.Player(self.pl_last_x, self.pl_last_y)
        self.clock = pygame.time.Clock()
        self.level_num = 0
        self.state = 'START'
        self.last_state = 'START'
        self.main_menu = Menu()
        self.texts = []
        self.text1 = Text(200, 150, 400, 50, 'Движение:')
        self.text2 = Text(200, 200, 400, 50, 'Стрельба:                      ЛКМ')
        self.text3 = Text(200, 250, 400, 50, 'Пауза во время игры: ESC')
        self.text4 = Text(200, 300, 400, 50, '')
        self.texts = [self.text1, self.text2, self.text3]
        self.game_over = pygame.image.load('images/Over.png')
        self.button_sound = pygame.mixer.Sound('sounds/button sound.ogg')
        self.button_sound.set_volume(2.8)
        self.save = True

    def create_level(self):
        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.player)
        self.player.rect.x, self.player.rect.y = self.levels.load_level(self.level_num)
        self.main_menu.create()
        if self.level_num > 0:
            self.player.rect.x, self.player.rect.y = self.pl_last_x, self.pl_last_y
        self.enemy_list = pygame.sprite.Group()
        if self.level_num == 0:
            pygame.mixer.music.load('sounds/into sandys city.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
        elif self.level_num == 3:
            pygame.mixer.music.load('sounds/at dooms gate.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
        for coord in self.levels.invader_coords:
            enemy = game_object.Green_invader(coord[0], coord[1])
            enemy.stop = coord[2]
            self.enemy_list.add(enemy)
            self.all_sprite_list.add(enemy)
        for coord in self.levels.bl_invader_coords:
            enemy = game_object.Blue_invader(coord[0], coord[1])
            enemy.stop = coord[2]
            self.enemy_list.add(enemy)
            self.all_sprite_list.add(enemy)
        for coord in self.levels.red_invader_coords:
            enemy = game_object.Red_invader(coord[0], coord[1])
            enemy.stop = coord[2]
            self.enemy_list.add(enemy)
            self.all_sprite_list.add(enemy)
        for coord in self.levels.volt_coords:
            enemy = game_object.Volt(coord[0], coord[1])
            enemy.stop = coord[2]
            self.enemy_list.add(enemy)
            self.all_sprite_list.add(enemy)

    def handle_scene(self, event):
        if self.state == "GAME":
            if self.player.control_type == 'mouse':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.player.cooldown <= 0:
                            self.player.shot()
                            self.player.cooldown = 0
                            self.player.cooldown = FPS

            elif self.player.control_type == 'WASD':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.player.cooldown <= 0:
                            self.player.shot()
                            self.player.cooldown = 0
                            self.player.cooldown = FPS
                    if event.key == pygame.K_a:
                        self.player.go_left()
                    if event.key == pygame.K_d:
                        self.player.go_right()
                    if event.key == pygame.K_w:
                        self.player.go_up()
                    if event.key == pygame.K_s:
                        self.player.go_down()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        if self.player.change_x < 0:
                            self.player.stop('gor')
                    if event.key == pygame.K_d:
                        if self.player.change_x > 0:
                            self.player.stop('gor')
                    if event.key == pygame.K_w:
                        if self.player.change_y < 0:
                            self.player.stop('ver')
                    if event.key == pygame.K_s:
                        if self.player.change_y > 0:
                            self.player.stop('ver')
        elif self.state == "OVER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.state = "GAME"
                    if not self.save:
                        self.level_num = 3
                    self.create_level()
                    self.player.rect.centerx, self.player.rect.y = 400, 720
        else:
            active_button = self.main_menu.handle_mouse_event(event.type)
            if active_button:
                self.button_sound.play()
                active_button.state = "normal"
                if active_button.name == "START":
                    self.level_num = 0
                    self.create_level()
                    self.state = "GAME"
                    self.type = 'pause'
                    self.main_menu.create()
                elif active_button.name == "CONTINUE":
                    self.state = "GAME"
                elif active_button.name == "OPTIONS":
                    self.state = "OPTIONS"
                    self.main_menu.menu_type = "options"
                    self.main_menu.create()
                    if self.save:
                        self.main_menu.buttons[1].text = self.main_menu.buttons[1].font.render('SAVE: ON', True, self.main_menu.buttons[1].font_color)
                    elif not self.save:
                        self.main_menu.buttons[1].text = self.main_menu.buttons[1].font.render('SAVE: OFF', True, self.main_menu.buttons[1].font_color)
                elif active_button.name == "CONTROLS":
                    self.state = 'CONTROLS'
                    self.main_menu.menu_type = 'controls'
                    self.main_menu.create()
                    if self.player.control_type == 'mouse':
                        self.main_menu.buttons[0].text = self.main_menu.buttons[0].font.render('MOUSE', True, self.main_menu.buttons[0].font_color)
                    if self.player.control_type == 'WASD':
                        self.main_menu.buttons[0].text = self.main_menu.buttons[0].font.render('WASD', True, self.main_menu.buttons[0].font_color)
                elif active_button.name == 'RETURN':
                    if self.state == 'CONTROLS':
                        self.state = 'OPTIONS'
                        self.main_menu.menu_type = 'options'
                        self.main_menu.create()
                        if self.save:
                            self.main_menu.buttons[1].text = self.main_menu.buttons[1].font.render('SAVE: ON', True, self.main_menu.buttons[1].font_color)
                        elif not self.save:
                            self.main_menu.buttons[1].text = self.main_menu.buttons[1].font.render('SAVE: OFF', True, self.main_menu.buttons[1].font_color)
                    elif self.state == 'OPTIONS':
                        self.state = self.last_state
                        if self.last_state == 'START':
                            self.main_menu.menu_type = 'main'
                        elif self.last_state == 'PAUSE':
                            self.main_menu.menu_type = 'pause'
                        self.main_menu.create()
                elif active_button.name == 'MOUSE':
                    self.player.control_type = 'WASD'
                    self.main_menu.buttons[0].name = 'WASD'
                    self.main_menu.buttons[0].text = self.main_menu.buttons[0].font.render(self.main_menu.buttons[0].name, True, self.main_menu.buttons[0].font_color)
                    self.text2.name = 'Стрельба:                      Пробел'
                elif active_button.name == 'WASD':
                    self.player.control_type = 'mouse'
                    self.main_menu.buttons[0].name = 'MOUSE'
                    self.main_menu.buttons[0].text = self.main_menu.buttons[0].font.render(self.main_menu.buttons[0].name, True, self.main_menu.buttons[0].font_color)
                    self.text2.name = 'Стрельба:                      ЛКМ'
                elif active_button.name == 'SAVE: ON':
                    self.save = False
                    self.main_menu.buttons[1].name = 'SAVE: OFF'
                    self.main_menu.buttons[1].text = self.main_menu.buttons[1].font.render(self.main_menu.buttons[1].name, True, self.main_menu.buttons[1].font_color)
                elif active_button.name == 'SAVE: OFF':
                    self.save = True
                    self.main_menu.buttons[1].name = 'SAVE: ON'
                    self.main_menu.buttons[1].text = self.main_menu.buttons[1].font.render(self.main_menu.buttons[1].name, True, self.main_menu.buttons[1].font_color)
                elif active_button.name == "QUIT":
                    pygame.quit()

    def draw(self):
        self.screen.fill(BLACK)
        if self.state == "START":
            self.main_menu.draw(self.screen)
        elif self.state == "GAME":
            self.all_sprite_list.draw(self.screen)
            self.player.pl_bullets.draw(self.screen)
            for enemy in self.enemy_list:
                enemy.en_bullets.draw(self.screen)
        elif self.state == "PAUSE":
            self.all_sprite_list.draw(self.screen)
            self.player.pl_bullets.draw(self.screen)
            for enemy in self.enemy_list:
                enemy.en_bullets.draw(self.screen)
            self.main_menu.draw(self.screen)
        elif self.state == "OPTIONS":
            self.main_menu.draw(self.screen)
        elif self.state == "CONTROLS":
            for text in self.texts:
                text.draw(self.screen)
            self.main_menu.draw(self.screen)
        elif self.state == "OVER":
            self.screen.blit(self.game_over, (0, 0))

    def run(self):
        self.main_menu.create()
        done = False
        self.create_level()
        while not done:
            for event in pygame.event.get():
                print(pygame.event.get())
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "GAME":
                            button = self.main_menu.buttons[0]
                            button.name = "CONTINUE"
                            button.text = button.font.render("CONTINUE", True, button.font_color)
                            self.state = "PAUSE"
                            self.last_state = "PAUSE"
                            self.player.change_x, self.player.change_y = 0, 0
                self.handle_scene(event)
            if self.state == "GAME":
                self.all_sprite_list.update()
                self.player.pl_bullets.update()
                for text in self.texts:
                    text.update()
                for enemy in self.enemy_list:
                    enemy.en_bullets.update()
                enemyCollisions = pygame.sprite.groupcollide(self.enemy_list, self.player.pl_bullets, False, True)
                for enemy in enemyCollisions:
                    enemy.hp -= 1
                for enemy in self.enemy_list:
                    playerCollisions = pygame.sprite.spritecollide(self.player, enemy.en_bullets, True)
                    for collisions in playerCollisions:
                        self.state = 'OVER'
                        self.player.change_x, self.player.change_y = 0, 0
                if self.level_num != 3:
                    if len(self.enemy_list) == 0:
                        self.level_num += 1
                        self.pl_last_x, self.pl_last_y = self.player.rect.x, self.player.rect.y
                        self.create_level()
                        self.player.stop('gor')
                        self.player.stop('ver')
            else:
                if self.state == "CONTROLS":
                    for text in self.texts:
                        text.update()  
                self.main_menu.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()     
game = Game()
game.run()
