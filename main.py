import pygame
from board import Board
from config import BLACK, WHITE, GREEN, RED, display_width, display_height, SIZE, PADDING


def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048)

    pygame.mixer.init()
    pygame.init()
    pygame.font.init()

    display = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()

    board = Board(display)
    board.create_board(display)
    board.create_piece()

    while board.Run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.Run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if board.Releas['main']:
                        board.func(event.pos)

                    if board.what_releas(event.pos) and not board.Releas['win']:
                        board.play_esc()
                        board.Releas['main'] = not board.Releas['main']

                    elif board.a == 2:
                        board.func(event.pos)

                    elif not board.Releas['main'] or not board.Releas['win']:
                        board.select(event.pos[0]//SIZE*SIZE,
                                     event.pos[1]//SIZE*SIZE)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and board.a != 2:
                    board.play_esc()
                    board.Releas['main'] = not board.Releas['main']

        board.create_board(display)
        board.draw_piece(display)
        board._king()
        board.__restart__(display)
        board.draw_static()
        board.impossiblity()
        board.win()

        if board.hover:
            for i in board.where_move(board.x, board.y):
                if board.get_piece(i[0], i[1]) == None:
                    pygame.draw.circle(
                        display, GREEN, (i[0]+SIZE//2, i[1]+SIZE//2), 15)
            for i in board.pieces:
                if i.select:
                    pygame.draw.circle(
                        display, GREEN, (i.row+SIZE//2, i.coll+SIZE//2), 15)
            for i in board.bite(board.x, board.y):
                pygame.draw.circle(display, GREEN, (i[2]+SIZE//2, i[3]+50), 15)
                pygame.draw.circle(
                    display, RED, (i[0]+SIZE//2, i[1]+SIZE//2), 15)

        if board.Releas['main']:
            board.draw_stop_menu()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
