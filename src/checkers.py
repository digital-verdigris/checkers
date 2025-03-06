import pygame
from server import checkers_server
from board import checkers_board

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8,8
SQUARE_SIZE = 512 // 8

#pygame initialization
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("verdigris checkers")

class checkers_game:
    def __init__(self):
        self.game_board = checkers_board()
        self.running = True
        self.clock = pygame.time.Clock()
        self.server = checkers_server()
    
    def game_loop(self):
        while self.running:
            self.clock.tick(60)  #60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    col = (mouse_x // SQUARE_SIZE) - 1
                    row = (mouse_y // SQUARE_SIZE) - 1

                    if (col >= 0 and col <= 7) and (row >= 0 and row <= 7):
                        if self.game_board._selected_piece is None:
                            self.game_board.select_piece(row, col)
                        else:
                            if self.game_board.move_piece(self.game_board._selected_pos[0],self.game_board._selected_pos[1], row, col):
                                self.game_board.print_board()
                            self.game_board.deselect_piece()

            if self.game_board.check_win():
                self.running = False

            self.game_board.draw_board(WINDOW)
            pygame.display.update()
        pygame.quit()

def main():
    game = checkers_game()
    game.game_loop()

if __name__ == "__main__":
    main()