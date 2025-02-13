import pygame

#constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8,8
SQUARE_SIZE = WIDTH // COLS

WHITE = (255,255,255)
GRAY  = (150,150,150)
BLACK = (0,0,0)
RED   = (255,0,0)
GREEN = (0,255,0)
#pygame initialization
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

#piece class
class piece:
    #setup
    def __init__(self, team):
        self._team = team
        self._is_king = False
        self._is_selected = False

    #print to terminal
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
    
    #to set king if needed
    def make_king(self):
        self._is_king = True
    
    def get_king_status(self):
        return self._is_king
    
    def set_selected(self, state):
        self._is_selected = state
    
    #to draw the piece onto the pygame display
    def draw(self, window, row, col):
        color = RED if self._team == 'red' else BLACK

        #if piece is selected, draw green circle under it
        if self._is_selected:
            pygame.draw.circle(window, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2)
        
        #draw the piece at the location
        pygame.draw.circle(window, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
        
        #if king draw white circle ontop of piece
        if self._is_king:
            pygame.draw.circle(window, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 8)

#board class
class board:
    #init the board
    def __init__(self):
        self._grid = [[' ' for _ in range(8)] for _ in range(8)]
        self._selected_piece = None
        self._selected_pos = None

        #set the initial piece layout
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self._grid[row][col] = piece('red')

                    elif row > 4:
                        self._grid[row][col] = piece('black')

                    else:
                        self._grid[row][col] = '.'

    #print the board to terminal
    def print_board(self):
        for row_idx, row in enumerate(self._grid):
            for col_idx, cell in enumerate(row):
                if isinstance(cell, piece):
                    cell.print()
                else:
                    print(cell, end = ' ')
            print()

    #draw the board in pygame display
    def draw_board(self, window):
        window.fill(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(window, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                piece_at_cell = self._grid[row][col]
                if isinstance(piece_at_cell, piece):
                    piece_at_cell.draw(window, row, col)
    
    def select_piece(self, row, col):
        piece_at_cell = self._grid[row][col]
        if isinstance (piece_at_cell, piece):
            self._selected_piece = piece_at_cell
            self._selected_pos = (row, col)
            piece_at_cell.set_selected(True)

    def move_piece(self, row, col):
        if self._selected_piece:
            old_row, old_col = self._selected_pos

            if self.is_valid_move(old_row, old_col, row, col):
                self._grid[row][col] = self._selected_piece
                self._grid[old_row][old_col] = '.'
                self._selected_piece.set_selected(False)
                self._selected_piece = None
                self._selected_pos = None

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        piece_to_move = self._grid[start_row][start_col]
        target = self._grid[end_row][end_col]

        if target != '.':
            return False

        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)

        if not piece_to_move.get_king_status():
            if row_diff == 1 and col_diff == 1:
                if piece_to_move._team == 'red' and end_row > start_row:
                    return True
                elif piece_to_move._team == 'black' and end_row < start_row:
                    return True
                return False
        
        if row_diff == 2 and col_diff == 2:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            middle_piece = self._grid[middle_row][middle_col]
            if isinstance(middle_piece, piece) and middle_piece._team != piece_to_move._team:
                if piece_to_move._team == 'red' and end_row > start_row:
                    self._grid[middle_row][middle_col] = '.'
                    return True
                elif piece_to_move._team == 'black' and end_row < start_row:
                    self._grid[middle_row][middle_col] = '.'
                    return True
                return False

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
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col = mouse_x // SQUARE_SIZE
                row = mouse_y // SQUARE_SIZE

                if game_board._selected_piece is None:
                    game_board.select_piece(row, col)
                else:
                    game_board.move_piece(row, col)

        game_board.draw_board(WINDOW)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()