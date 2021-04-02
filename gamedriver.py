from checkers import Checker
import pygame
import os
from pygame import mixer
from config import BLACK, WHITE, GREEN, RED, display_width, display_height, SIZE, PADDING


class Button:
    def __init__(self, display, xy, wh, pading_x_y, color_f, color_t, text, size: int):
        self.display = display
        self.pading_x_y = pading_x_y
        self.xy, self.wh = xy, wh
        self.color_f, self.color_t = color_f, color_t
        self.text, self.size = text, size

        font_ = pygame.font.SysFont("comicsansms", self.size)
        text_ = font_.render(self.text, 0, self.color_t)

        pygame.draw.rect(display, self.color_f, (self.xy, self.wh))
        self.display.blit(
            text_, (self.xy[0]+self.pading_x_y[0], self.xy[1]+self.pading_x_y[1]))


class Music:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        # pygame.init()

        self.bite_music = pygame.mixer.Sound(
            os.getcwd()+"\sound\when_piece_bited.ogg")
        self.step_music = pygame.mixer.Sound(os.getcwd()+"\sound\step22.ogg")
        self.esc_music = pygame.mixer.Sound(os.getcwd()+"\sound\menu2.ogg")
        self.win_music = pygame.mixer.Sound(os.getcwd()+"\sound\win2.ogg")
        self.a = 1

    def play_step(self):
        self.step_music.play()

    def play_eat(self):
        self.bite_music.play()

    def play_esc(self):
        self.esc_music.play()

    def play_win(self):
        self.win_music.play()


class GameDriver(Checker, Music):
    def __init__(self, display):
        Music.__init__(self)
        self.display = display
        self.buttons = []
        # self.black_point = 0
        # self.white_point = 0
        self.point = {'BLACK': 0, 'WHITE': 0}
        self.piece_position = []
        self.past_x_white = -50
        self.past_x_black = -50
        self._ico = {
            'xblack': pygame.image.load(os.getcwd()+"\img\gg.png"),
            'xwhite': pygame.image.load(os.getcwd()+"\img\ggg.png"),
            'font': pygame.image.load(os.getcwd()+'\img\green.jpg'),
            'menu_ico': pygame.image.load(os.getcwd()+"\img\menu.png"),
            'game_font': pygame.image.load(os.getcwd()+"\img\game_font2.jpg"),
            'cup': pygame.image.load(os.getcwd()+"\img\cup.png")
        }
        self.Run = True
        self.Releas = {'main': False, 'win': False}
        self.restart_signal = False
        self.win_timer = False
        self.defoul_font = pygame.font.SysFont("comicsansms", 39)
        self.last = "BLACK"

    def update_point(self, color):
        if color == "BLACK":
            self.point['BLACK'] += 1
            self.piece_position.append(
                Checker(display_width+82, self.past_x_black+60, color))
            self.past_x_black += 60
        else:
            self.point['WHITE'] += 1
            self.piece_position.append(
                Checker(display_width+82, self.past_x_white+60, color))
            self.past_x_white += 60

    def win(self):
        if 12 in self.point.values() or self.win_timer == True:
            self.buttons.clear()
            self.display.blit(self._ico['game_font'], (110, 90))
            restart_ = Button(self.display, (290, 500), (200, 80),
                              (40, 17), BLACK, WHITE, 'Restart', 32)
            self.buttons.append(restart_)
            Close_Game = Button(self.display, (290, 630), (200, 80),
                                (20, 17), BLACK, WHITE, 'Close game', 32)
            self.buttons.append(Close_Game)
            for l, k in self.point.items():
                if k >= 12:
                    text = self.defoul_font.render(
                        l+' pieces are Win', 0, (0, 0, 0))
            if self.win_timer:
                text = self.defoul_font.render(
                    self.last+' pieces are Win', 0, (0, 0, 0))

            self.display.blit(self._ico['cup'], (310, 150))
            self.display.blit(text, (200, 340))
            self.Releas['win'] = True
            if self.a == 1:
                self.play_win()
                self.a = 2

    def draw_static(self):
        self.display.blit(self._ico['font'], (0, display_width))
        self.display.blit(self._ico['menu_ico'], (720, display_width))
        pygame.draw.line(self.display, BLACK, [
                         0, display_width+1], [display_width, display_width+1], 3)
        pygame.draw.line(self.display, BLACK, [1, 0], [1, display_height], 3)
        pygame.draw.line(self.display, BLACK, [
                         0, display_height-1], [display_width, display_height-1], 3)
        pygame.draw.line(self.display, BLACK, [
                         display_width-2, 0], [display_width-2, display_height], 3)
        pygame.draw.line(self.display, BLACK, [0, 1], [display_width, 1], 3)

        for i in self.piece_position:
            if i.color == "BLACK":
                i.checker = self._ico['xwhite']
            else:
                i.checker = self._ico['xblack']

            self.display.blit(i.checker, (i.row, i.coll))

    def what_releas(self, cord):  # (724, 829) (767, 863)
        x, y = cord
        if x >= 720 and x <= 777:
            if y >= display_width and y <= 873:
                return True

    def draw_stop_menu(self):
        self.buttons.clear()
        self.display.blit(self._ico['game_font'], (110, 90))
        continue_ = Button(self.display, (290, 290), (200, 80),
                           (25, 17), (0, 0, 0), (255, 255, 255), 'Continue', 32)
        restart_ = Button(self.display, (290, 420), (200, 80),
                          (40, 17), (0, 0, 0), (255, 255, 255), 'Restart', 32)
        Close_Game = Button(self.display, (290, 550), (200, 80),
                            (20, 17), (0, 0, 0), (255, 255, 255), 'Close game', 32)

        self.buttons.append(restart_)
        self.buttons.append(Close_Game)
        self.buttons.append(continue_)

    def func(self, cord):
        x, y = cord
        for i in self.buttons:
            if x >= i.xy[0] and x <= i.xy[0] + i.wh[0]:
                if y >= i.xy[1] and y <= i.xy[1] + i.wh[1]:
                    if i.text == "Close game":
                        self.Run = False
                        return

                    elif i.text == "Continue":
                        self.Releas['main'] = False
                        self.Releas['win'] = False
                        return

                    elif i.text == "Restart":
                        self.restart_signal = True
                        return
