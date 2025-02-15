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
BLUE  = (0,0,255)
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
    
#board class
class board:
    #init the board
    def __init__(self):
        self._grid = [[' ' for _ in range(8)] for _ in range(8)]
        self._selected_piece = None
        self._selected_pos = None
        self._valid_moves = None
        self._red_count = 12
        self._black_count = 12

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

        self.update_valid_pieces()

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
                        if (row, col) in self._valid_pieces:
                            pygame.draw.circle(window, BLUE,(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2.5)

                        color = RED if piece_at_cell._team == 'red' else BLACK
                        pygame.draw.circle(window, color,(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
                        
                        if piece_at_cell._is_king:
                            pygame.draw.circle(window, WHITE,(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),SQUARE_SIZE // 8)

        if self._valid_moves:
            for chain in self._valid_moves:
                for i in range(1, len(chain)):  
                    row, col = chain[i]
                    color = GREEN if i == len(chain) - 1 else WHITE
                    pygame.draw.circle(window, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 4) 
        
        if self._selected_pos:
            row, col = self._selected_pos
            pygame.draw.circle(window, GREEN,(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),SQUARE_SIZE // 2, 3)
    
    def update_valid_pieces(self):
        self._valid_pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece_at_cell = self._grid[row][col]
                if isinstance(piece_at_cell, piece):
                    valid_moves = self.get_valid_moves(row, col)
                    if valid_moves:
                        self._valid_pieces.append((row, col))
        print(self._valid_pieces)

    def get_valid_moves(self, row, col):
        piece_to_move = self._grid[row][col]
        valid_move_chains = []

        if not isinstance(piece_to_move, piece):
            return valid_move_chains

        directions = []
        if piece_to_move._team == 'red' or piece_to_move.get_king_status():
            directions.append((1, -1))  #down-left
            directions.append((1, 1))   #down-right
        if piece_to_move._team == 'black' or piece_to_move.get_king_status():
            directions.append((-1, -1)) #up-left
            directions.append((-1, 1))  #up-right

        def find_jumps(row, col, current_chain, visited):
            jumped = False

            for direction in directions:
                new_row = row + direction[0] * 2
                new_col = col + direction[1] * 2
                middle_row = row + direction[0]
                middle_col = col + direction[1]

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if 0 <= middle_row < 8 and 0 <= middle_col < 8:
                        middle_piece = self._grid[middle_row][middle_col]

                    if self._grid[new_row][new_col] == '.' and isinstance(middle_piece, piece) and middle_piece._team != piece_to_move._team:
                        if (new_row, new_col) not in visited:
                            visited.add((new_row, new_col))
                            new_chain = current_chain + [(new_row, new_col)]
                            jumped = True
                            find_jumps(new_row, new_col, new_chain, visited)

            if not jumped and len(current_chain) > 1:
                valid_move_chains.append(current_chain)
        
        find_jumps(row, col, [(row, col)], set([(row, col)]))

        if not valid_move_chains:
            for direction in directions:
                new_row = row + direction[0]
                new_col = col + direction[1]

                if 0 <= new_row < 8 and 0 <= new_col < 8 and self._grid[new_row][new_col] == '.':
                    valid_move_chains.append([(row, col), (new_row, new_col)])
        
        print(valid_move_chains)
        return valid_move_chains

    def select_piece(self, row, col):
        piece_at_cell = self._grid[row][col]
        if isinstance (piece_at_cell, piece):
            self._selected_piece = piece_at_cell
            self._selected_pos = (row, col)
            self._valid_moves = self.get_valid_moves(row, col)

    def deselect_piece(self):
        self._selected_piece = None
        self._selected_pos = None
        self._valid_moves = None
        self.update_valid_pieces()

    def move_piece(self, start_row, start_col, end_row, end_col):
        piece_to_move = self._grid[start_row][start_col]
        piece_at_dest = self._grid[end_row][end_col]

        if not isinstance(piece_to_move, piece) or piece_at_dest != '.':
            return False

        valid_moves = self.get_valid_moves(start_row, start_col)
            
        for chain in valid_moves:
            if (end_row, end_col) in chain:
                move_distance = abs(start_row - end_row)

                if len(chain) > 2:
                    if chain[-1] == (end_row, end_col):
                        self._grid[end_row][end_col] = piece_to_move
                        self._grid[start_row][start_col] = '.'

                        for i in range(1, len(chain)):
                            middle_row = (chain[i-1][0] + chain[i][0]) // 2
                            middle_col = (chain[i-1][1] + chain[i][1]) // 2
                            middle_piece = self._grid[middle_row][middle_col]
                            if isinstance(middle_piece, piece):
                                self._grid[middle_row][middle_col] = '.'
                                if middle_piece._team == 'red':
                                    self._red_count -= 1
                                elif middle_piece._team == 'black':
                                    self._black_count -= 1

                elif move_distance == 1:
                    if chain[-1] == (end_row, end_col):
                        self._grid[end_row][end_col] = piece_to_move
                        self._grid[start_row][start_col] = '.'
                        
                        if (piece_to_move._team == 'red' and end_row == 7) or (piece_to_move._team == 'black' and end_row == 0):
                            piece_to_move.make_king()
                        return True
                        
                elif move_distance == 2:
                    if chain[-1] == (end_row, end_col):
                        self._grid[end_row][end_col] = piece_to_move
                        self._grid[start_row][start_col] = '.'

                        middle_row = (start_row + end_row) // 2
                        middle_col = (start_col + end_col) // 2
                        middle_piece = self._grid[middle_row][middle_col]
                        if isinstance(middle_piece, piece):
                                self._grid[middle_row][middle_col] = '.'
                                if middle_piece._team == 'red':
                                    self._red_count -= 1
                                elif middle_piece._team == 'black':
                                    self._black_count -= 1

                        if (piece_to_move._team == 'red' and end_row == 7) or (piece_to_move._team == 'black' and end_row == 0):
                            piece_to_move.make_king()
                        return True
        return False

    def check_win(self):
        if self._red_count == 0:
            return True
        if self._black_count == 0:
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
                    if game_board.move_piece(game_board._selected_pos[0], game_board._selected_pos[1], row, col):
                        game_board.print_board()
                    game_board.deselect_piece()

        if game_board.check_win():
            running = False

        game_board.draw_board(WINDOW)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()