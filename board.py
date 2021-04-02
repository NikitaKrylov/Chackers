import pygame
from config import BLACK, WHITE, GREEN, display_width, display_height, SIZE, PADDING
from math import fabs
from checkers import Checker
from gamedriver import GameDriver, Music


class Board(GameDriver):
    def __init__(self, display):
        self.display = display
        GameDriver.__init__(self, self.display)
        self.x = -1
        self.y = -1
        self.selected = True
        self.hover = False
        self.all_piec_cord = []
        self.pieces = []
        self.move_place = []
        self.bited_piece = []

    def create_board(self, display):
        display.fill((255, 255, 255))
        for row in range(8):
            for coll in range(row % 2, 8, 2):
                pygame.draw.rect(
                    self.display, BLACK, (row*SIZE, coll*SIZE, SIZE, SIZE))

                self.all_piec_cord.append((row*SIZE, coll*SIZE))

    def create_piece(self):
        for i in self.all_piec_cord[:12]:
            self.pieces.append(Checker(i[0], i[1], "WHITE"))

        for i in self.all_piec_cord[::-1][:12]:
            self.pieces.append(Checker(i[0], i[1], "BLACK"))

    def draw_piece(self, display):
        for i in self.pieces:
            self.display.blit(i.checker, (i.row+PADDING, i.coll+PADDING))

    def get_piece(self, row, coll):
        for i in self.pieces:
            if i.row == row and i.coll == coll:
                return i

    def reset(self):
        if self.last == "BLACK":
            self.last = 'WHITE'
        else:
            self.last = 'BLACK'

    def where_move(self, x, y):
        self.move_place.clear()
        if self.get_piece(x, y):
            del_ = []
            object = self.get_piece(x, y)

            if object.king:
                if self.get_piece(x-SIZE, y+SIZE) == None:
                    self.move_place.append((x-SIZE, y+SIZE))

                if self.get_piece(x+SIZE, y+SIZE) == None:
                    self.move_place.append((x+SIZE, y+SIZE))

                if self.get_piece(x-SIZE, y-SIZE) == None:
                    self.move_place.append((x-SIZE, y-SIZE))

                if self.get_piece(x+SIZE, y-SIZE) == None:
                    self.move_place.append((x+SIZE, y-SIZE))

            else:
                if object.color == "WHITE":
                    if self.get_piece(x-SIZE, y+SIZE) == None:
                        self.move_place.append((x-SIZE, y+SIZE))

                    if self.get_piece(x+SIZE, y+SIZE) == None:
                        self.move_place.append((x+SIZE, y+SIZE))

                elif object.color == "BLACK":
                    if self.get_piece(x-SIZE, y-SIZE) == None:
                        self.move_place.append((x-SIZE, y-SIZE))

                    if self.get_piece(x+SIZE, y-SIZE) == None:
                        self.move_place.append((x+SIZE, y-SIZE))

            for i in self.move_place:
                for num in i:
                    if 0 > num or display_width-SIZE < num:
                        del_.append(i)
                        break

            for i in del_:
                self.move_place.remove(i)

        return self.move_place

    def bite(self, x, y):
        self.bited_piece.clear()
        object = self.get_piece(x, y)

        if self.get_piece(x-SIZE, y-SIZE) != None and object.color != self.get_piece(x-SIZE, y-SIZE).color:
            if not self.get_piece(x-SIZE*2, y-SIZE*2):
                self.bited_piece.append((x-SIZE, y-SIZE, x-SIZE*2, y-SIZE*2))

        if self.get_piece(x+SIZE, y-SIZE) != None and object.color != self.get_piece(x+SIZE, y-SIZE).color:
            if not self.get_piece(x+SIZE*2, y-SIZE*2):
                self.bited_piece.append((x+SIZE, y-SIZE, x+SIZE*2, y-SIZE*2))

        if self.get_piece(x+SIZE, y+SIZE) != None and object.color != self.get_piece(x+SIZE, y+SIZE).color:
            if not self.get_piece(x+SIZE*2, y+SIZE*2):
                self.bited_piece.append((x+SIZE, y+SIZE, x+SIZE*2, y+SIZE*2))

        if self.get_piece(x-SIZE, y+SIZE) != None and object.color != self.get_piece(x-SIZE, y+SIZE).color:
            if not self.get_piece(x-SIZE*2, y+SIZE*2):
                self.bited_piece.append((x-SIZE, y+SIZE, x-SIZE*2, y+SIZE*2))

        del_ = []
        for i in self.bited_piece:
            for num in i:
                if display_width-SIZE < num or 0 > num:
                    del_.append(i)
                    break
        for i in del_:
            self.bited_piece.remove(i)

        return self.bited_piece

    def __move__(self, xpos, ypos, x, y):
        object = self.get_piece(xpos, ypos)
        object.row, object.coll = x, y

    def _king(self):
        for i in self.pieces:
            if i.color == "BLACK" and i.coll == 0:
                i.make_king()
            elif i.color == "WHITE" and i.coll == display_width-SIZE:
                i.make_king()

    def __restart__(self, display):
        if self.restart_signal:
            self.__init__(display)
            self.create_board(display)
            self.create_piece()

    def select(self, xpos, ypos):
        if (xpos, ypos) in self.all_piec_cord:
            if self.y == ypos and self.x == xpos:  # второй отменяющий клик
                self.x, self.y = -1, -1
                self.selected = True
                self.hover = False
                self.get_piece(xpos, ypos).select = False

            elif self.x != xpos and self.y != ypos:
                for i in self.bite(self.x, self.y):
                    if i[2] == xpos and i[3] == ypos:  # клик для передвижения с ударом
                        self.play_eat()
                        self.pieces.remove(self.get_piece(i[0], i[1]))
                        self.selected, self.hover = True, False
                        obj = self.get_piece(self.x, self.y)
                        obj.select = False
                        self.update_point(obj.color)
                        self.__move__(self.x, self.y, xpos, ypos)

                        if self.bite(xpos, ypos):
                            self.selected, self.hover = True, True
                            continue

                        self.x, self.y = -1, -1
                        self.reset()
                        return None

                if (xpos, ypos) in self.where_move(self.x, self.y):
                    if not self.get_piece(xpos, ypos):  # клик для передвижения
                        self.play_step()
                        self.selected, self.hover = True, False
                        self.get_piece(self.x, self.y).select = False
                        self.__move__(self.x, self.y, xpos, ypos)
                        self.x, self.y = -1, -1
                        self.reset()

                elif self.selected:  # первый клик
                    ob = self.get_piece(xpos, ypos)
                    if ob:
                        if ob.color == self.last:
                            self.get_piece(xpos, ypos).select = True
                            self.selected, self.hover = False, True
                            self.x, self.y = xpos, ypos
                            self.bite(xpos, ypos)

    def impossiblity(self):
        if not self.win_timer:
            t = 0
            for i in self.pieces:
                if i.color == self.last:
                    if len(self.where_move(i.row, i.coll)) > 0:
                        t += 1
                    if len(self.bite(i.row, i.coll)) > 0:
                        t += 1
            if t == 0:
                self.win_timer = True
                self.reset()
