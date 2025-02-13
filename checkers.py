import pygame

#constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8,8
SQUARE_SIZE = WIDTH // COLS

WHITE = (255,255,255)
GRAY =  (150,150,150)
BLACK = (0,0,0)
RED =   (255,0,0)

#pygame initialization
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

#piece class
class piece:
    def __init__(self, team):
        self._team = team
        self._is_king = False
    
    def print(self):
        if self._team == 'red':
            name = 'R'
        elif self._team == 'black':
            name = 'B'
        else:
            name = '?'
            
        if not self._is_king:
            print(name, end = ' ')
        else:
            print(f"{name}K", end = ' ')
    
    def make_king(self):
        self._is_king = True
    
    def draw(self, window, row, col):
        color = RED if self._team == 'red' else BLACK
        pygame.draw.circle(window, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
        if self._is_king:
            pygame.draw.circle(window, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 8)

class board:
    def __init__(self):
        self.grid = [[' ' for _ in range(8)] for _ in range(8)]

        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.grid[row][col] = piece('red')

                    elif row > 4:
                        self.grid[row][col] = piece('black')

                    else:
                        self.grid[row][col] = '.'

    def print_board(self):
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                if isinstance(cell, piece):
                    cell.print()
                else:
                    print(cell, end = ' ')
            print()
    
    def draw_board(self, window):
        window.fill(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(window, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                piece_at_cell = self.grid[row][col]
                if isinstance(piece_at_cell, piece):
                    piece_at_cell.draw(window, row, col) 
def main():
    game_board = board()
    game_board.print_board()
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)  # 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game_board.draw_board(WINDOW)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()