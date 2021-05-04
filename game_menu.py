import pygame
from constants import *


class Button():
    def __init__(
            self, x, y, w, h, name,
            font_color=WHITE,
            normal_color=BLUE,
            highlight_color=GREEN,
            active_color=YELLOW,
            size=24,
            font='Arial',
            paddingx=5, paddingy=5
    ):
        self.state = 'normal'
        self.normal_color = normal_color
        self.highlight_color = highlight_color
        self.active_color = active_color
        self.name = name
        self.font_color = font_color
        pygame.font.init()
        self.font = pygame.font.SysFont(font, size, True)
        self.text = self.font.render(name, True,  font_color)
        self.image = pygame.Surface([w, h])
        self.image.fill(normal_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.paddingx = paddingx
        self.paddingy = paddingy

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, (self.rect.x + self.paddingx, self.rect.y + self.paddingy))

    def update(self):
        if self.state == 'normal':
            self.image.fill(self.normal_color)
        elif self.state == 'highlight':
            self.image.fill(self.highlight_color)
        elif self.state == 'active':
            self.image.fill(self.active_color)

    def handle_mouse_action(self, event=None):
        pos_x, pos_y = pygame.mouse.get_pos()
        check_pos = self.rect.left <= pos_x <= self.rect.right and self.rect.top <= pos_y <= self.rect.bottom
        if event == pygame.MOUSEMOTION:
            if check_pos:
                self.state = 'highlight'
            else:
                self.state = 'normal'
        elif event == pygame.MOUSEBUTTONDOWN:
            if check_pos:
                self.state = 'active'
            else:
                self.state = 'normal'
        elif event == pygame.MOUSEBUTTONUP:
            if check_pos:  
                self.state = 'highlight'
            else: 
                self.state = 'normal'


class Text():
    def __init__(self, x, y, w, h, name, color=WHITE, font_color=BLACK, size=22, font='Arial', padding=5):
        self.font = pygame.font.SysFont(font, size, True)
        self.font_color = BLACK
        self.name = name
        self.text = self.font.render(name, True,  font_color)
        self.image = pygame.Surface([w, h])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.padding = padding

    def update(self):
        self.text = self.font.render(self.name, True,  self.font_color)

    def draw(self, screen):
        screen.blit(self.image, self.rect)  
        screen.blit(self.text, (self.rect.x + self.padding, self.rect.y + self.padding))


class Menu():
    def __init__(self, w=300, h=200, menu_type='main'):
        self.menu_type = menu_type
        self.labels = []
        self.x = (WIN_WIDTH - w) // 2
        self.y = (WIN_HEIGHT - h) // 2
        self.buttons = []
        self.w = w
        self.h = h
        self.arw_crd = []

    def create(self):
        self.labels.clear()
        self.buttons.clear()
        if self.menu_type == 'main':
            self.labels = ['START', 'OPTIONS', 'QUIT']
            self.h = 200
        elif self.menu_type == 'pause':
            self.labels = ['CONTINUE', 'OPTIONS', 'QUIT']
            self.h = 200
        elif self.menu_type == 'options':
            self.labels = ['CONTROLS', 'SAVE: ON', 'RETURN']
            self.h = 200
        elif self.menu_type == 'controls':
            self.labels = ['MOUSE', 'RETURN']
            self.h = 150
        button_height = int(self.h / ((len(self.labels) + 1)))
        current_y = self.y
        if self.menu_type == 'main' or self.menu_type == 'options' or self.menu_type == 'pause':
            for label in self.labels:
                new_button = Button(self.x, current_y, self.w, button_height, label)
                current_y += button_height + 2
                self.buttons.append(new_button)
        elif self.menu_type == 'controls':
            for label in self.labels:
                if label == 'RETURN':
                    new_button = Button(200, 300, self.w, button_height, label)
                elif label == 'MOUSE':
                    new_button = Button(400, 150, 80, 40, label)
                self.buttons.append(new_button)

    def update(self):
        for button in self.buttons:
            button.update()

    def handle_mouse_event(self, event):
        for button in self.buttons:
            button.handle_mouse_action(event)
            if button.state == 'active':
                return button

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)