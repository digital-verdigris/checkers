import pygame
from piece import checkers_piece

#constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8,8
SQUARE_SIZE = 512 // 8

WHITE = (255,255,255)
GRAY  = (150,150,150)
BLACK = (0,0,0)
RED   = (255,0,0)
GREEN = (55,148,110)
BLUE  = (0,0,255)
BROWN = (69,40,60)

#board class
class checkers_board:
    #init the board
    def __init__(self):
        self._grid = [[' ' for _ in range(8)] for _ in range(8)]
        self._selected_piece = None
        self._selected_pos = None
        self._valid_moves = None
        self._red_count = 12
        self._black_count = 12
        self._turn = 'black'
        self._team = None

        #load sprites

        #piece icons
        self.red_piece_img = pygame.image.load("assets/pngs/red_checker.png")
        self.black_piece_img = pygame.image.load("assets/pngs/black_checker.png")
        self.red_king_piece_img = pygame.image.load("assets/pngs/red_king_checker.png")
        self.black_king_piece_img = pygame.image.load("assets/pngs/black_king_checker.png")

        self.piece_select_img = pygame.image.load("assets/pngs/piece_select.png")

        self.dark_space_img = pygame.image.load("assets/pngs/dark_checker_space.png")
        self.light_space_img = pygame.image.load("assets/pngs/light_checker_space.png")
        
        self.chain_node_img = pygame.image.load("assets/pngs/chain_node.png")
        self.chain_select_img = pygame.image.load("assets/pngs/chain_select.png")
        self.select_img = pygame.image.load("assets/pngs/select.png")

        #turn icons
        self.red_turn_icon_img = pygame.image.load("assets/pngs/red_turn_icon.png")
        self.black_turn_icon_img = pygame.image.load("assets/pngs/black_turn_icon.png")

        #score icons
        self.r_score_img = pygame.image.load("assets/pngs/r_score_icon.png")
        self.b_score_img = pygame.image.load("assets/pngs/b_score_icon.png")

        #logo
        self.logo_img = pygame.image.load("assets/pngs/checkers_logo.png")

        #load textures
        self.felt_img = pygame.image.load("assets/textures/felt_texture.jpg")

        #scale to fit squares
        self.red_piece_img = pygame.transform.scale(self.red_piece_img, (SQUARE_SIZE, SQUARE_SIZE))
        self.black_piece_img = pygame.transform.scale(self.black_piece_img, (SQUARE_SIZE, SQUARE_SIZE))
        self.red_king_piece_img = pygame.transform.scale(self.red_king_piece_img, (SQUARE_SIZE, SQUARE_SIZE))
        self.black_king_piece_img = pygame.transform.scale(self.black_king_piece_img, (SQUARE_SIZE, SQUARE_SIZE))      
       
        self.piece_select_img = pygame.transform.scale(self.piece_select_img, (SQUARE_SIZE, SQUARE_SIZE))      

        self.dark_space_img = pygame.transform.scale(self.dark_space_img, (SQUARE_SIZE, SQUARE_SIZE))
        self.light_space_img = pygame.transform.scale(self.light_space_img, (SQUARE_SIZE, SQUARE_SIZE))
        
        self.chain_node_img = pygame.transform.scale(self.chain_node_img, (SQUARE_SIZE, SQUARE_SIZE))
        self.chain_select_img = pygame.transform.scale(self.chain_select_img, (SQUARE_SIZE, SQUARE_SIZE))
        self.select_img = pygame.transform.scale(self.select_img, (SQUARE_SIZE, SQUARE_SIZE))

        self.red_turn_icon_img = pygame.transform.scale(self.red_turn_icon_img, (SQUARE_SIZE, SQUARE_SIZE))
        self.black_turn_icon_img = pygame.transform.scale(self.black_turn_icon_img, (SQUARE_SIZE, SQUARE_SIZE))

        self.logo_img = pygame.transform.scale(self.logo_img, (SQUARE_SIZE * 2, SQUARE_SIZE))

        self.r_score_img = pygame.transform.scale(self.r_score_img, (SQUARE_SIZE, SQUARE_SIZE))
        self.b_score_img = pygame.transform.scale(self.b_score_img, (SQUARE_SIZE, SQUARE_SIZE))

        self.felt_img = pygame.transform.scale(self.felt_img, (WIDTH, HEIGHT))

        #set the initial piece layout
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self._grid[row][col] = checkers_piece('red')

                    elif row > 4:
                        self._grid[row][col] = checkers_piece('black')

                    else:
                        self._grid[row][col] = '.'

        self.update_valid_pieces()

    #print the board to terminal
    def print_board(self):
        print('---------------')
        for row_idx, row in enumerate(self._grid):
            for col_idx, cell in enumerate(row):
                if isinstance(cell, checkers_piece):
                    cell.print()
                else:
                    print(cell, end = ' ')
            print()
        print('---------------')
        print()


    #draw the board in pygame display
    def draw_board(self, window):
        w_buffer = 64
        h_buffer = 64

        window.fill(GREEN)

        window.blit(self.felt_img, (0, 0))

        #window.blit(self.logo_img, (0, 0))

        pygame.draw.rect(window, BROWN, (62, 62, 516, 516))

        if self._turn == 'red':
                window.blit(self.red_turn_icon_img, (66, 4))

        elif self._turn == 'black':
                window.blit(self.black_turn_icon_img, (66, 4))

        for row in range(ROWS):
            for col in range(COLS):
                pos_x = col * SQUARE_SIZE + w_buffer
                pos_y = row * SQUARE_SIZE + h_buffer
                if (row + col) % 2 == 1: 
                    window.blit(self.dark_space_img, (pos_x, pos_y))
                else:                    
                    window.blit(self.light_space_img, (pos_x, pos_y))
                
                piece_at_cell = self._grid[row][col]

                if isinstance(piece_at_cell, checkers_piece):
                    if (row, col) in self._valid_pieces and not self._selected_piece and self._turn == self._team:
                        window.blit(self.select_img, (pos_x, pos_y))

                    if not piece_at_cell._is_king:
                        if piece_at_cell._team == 'red':
                            window.blit(self.red_piece_img, (pos_x, pos_y))
                        elif piece_at_cell._team == 'black':
                            window.blit(self.black_piece_img, (pos_x, pos_y))
                    
                    elif piece_at_cell._is_king:
                        if piece_at_cell._team == 'red':
                            window.blit(self.red_king_piece_img, (pos_x, pos_y))
                        elif piece_at_cell._team == 'black':
                            window.blit(self.black_king_piece_img, (pos_x, pos_y))

        if self._valid_moves:
            for chain in self._valid_moves:
                for i in range(1, len(chain)):  
                    row, col = chain[i]
                    pos_x = col * SQUARE_SIZE + w_buffer
                    pos_y = row * SQUARE_SIZE + h_buffer
                    if i == len(chain) - 1:
                        window.blit(self.chain_select_img, (pos_x, pos_y))
                    else: 
                        window.blit(self.chain_node_img, (pos_x, pos_y))
        
        if self._selected_pos:
            row, col = self._selected_pos
            pos_x = col * SQUARE_SIZE + w_buffer
            pos_y = row * SQUARE_SIZE + h_buffer
            window.blit(self.piece_select_img, (pos_x, pos_y))
    
    def update_valid_pieces(self):
        self._valid_pieces = []
        has_jump = False

        for row in range(ROWS):
            for col in range(COLS):
                piece_at_cell = self._grid[row][col]

                if isinstance(piece_at_cell, checkers_piece):
                    valid_moves = self.get_valid_moves(row, col)
                    if valid_moves:
                        if abs(valid_moves[0][0][0] - valid_moves[0][1][0]) == 2:
                            if has_jump:
                                if self._turn == 'black' and piece_at_cell._team == 'black':
                                    self._valid_pieces.append((row,col))
                            
                                elif self._turn == 'red' and piece_at_cell._team == 'red':
                                    self._valid_pieces.append((row,col))
                            else:
                                if self._turn == 'black' and piece_at_cell._team == 'black':
                                    has_jump = True
                                    self._valid_pieces = []
                                    self._valid_pieces.append((row,col))
                            
                                elif self._turn == 'red' and piece_at_cell._team == 'red':
                                    has_jump = True
                                    self._valid_pieces = []
                                    self._valid_pieces.append((row,col))
                        
                        if not has_jump:
                            if self._turn == 'black' and piece_at_cell._team == 'black':
                                self._valid_pieces.append((row,col))
                            
                            elif self._turn == 'red' and piece_at_cell._team == 'red':
                                self._valid_pieces.append((row,col))


    def get_valid_moves(self, row, col):
        piece_to_move = self._grid[row][col]
        valid_move_chains = []

        if not isinstance(piece_to_move, checkers_piece):
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

                    if self._grid[new_row][new_col] == '.' and isinstance(middle_piece, checkers_piece) and middle_piece._team != piece_to_move._team:
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
        
        return valid_move_chains

    def select_piece(self, row, col):
        piece_at_cell = self._grid[row][col]
        if isinstance (piece_at_cell, checkers_piece):
            if (row, col) in self._valid_pieces:
                self._selected_piece = piece_at_cell
                self._selected_pos = (row, col)
                self._valid_moves = self.get_valid_moves(row, col)

    def deselect_piece(self):
        self._selected_piece = None
        self._selected_pos = None
        self._valid_moves = []
        self.update_valid_pieces()

    def validate_move(self, move):
        start_row = move[0]
        start_col = move[1]
        end_row = move[2]
        end_col = move[3]

        piece_to_move = self._grid[start_row][start_col]
        piece_at_dest = self._grid[end_row][end_col]

        if not isinstance(piece_to_move, checkers_piece) or piece_at_dest != '.':
            return False

        valid_moves = self.get_valid_moves(start_row, start_col)
    
        for chain in valid_moves:
            if chain[-1] == (end_row, end_col):
                return True  
        return False

    def move_piece(self, move):
        start_row = move[0]
        start_col = move[1]
        end_row = move[2]
        end_col = move[3]

        piece_to_move = self._grid[start_row][start_col]
        piece_at_dest = self._grid[end_row][end_col]

        if not isinstance(piece_to_move, checkers_piece) or piece_at_dest != '.':
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
                            if isinstance(middle_piece, checkers_piece):
                                self._grid[middle_row][middle_col] = '.'
                                if middle_piece._team == 'red':
                                    self._red_count -= 1
                                elif middle_piece._team == 'black':
                                    self._black_count -= 1
                        
                        if (piece_to_move._team == 'red' and end_row == 7) or (piece_to_move._team == 'black' and end_row == 0):
                            piece_to_move.make_king()
                        
                        self.print_board()                       
                        return True

                elif move_distance == 1:
                    if chain[-1] == (end_row, end_col):
                        self._grid[end_row][end_col] = piece_to_move
                        self._grid[start_row][start_col] = '.'
                        
                        if (piece_to_move._team == 'red' and end_row == 7) or (piece_to_move._team == 'black' and end_row == 0):
                            piece_to_move.make_king()

                        self.print_board()
                        return True
                        
                elif move_distance == 2:
                    if chain[-1] == (end_row, end_col):
                        self._grid[end_row][end_col] = piece_to_move
                        self._grid[start_row][start_col] = '.'

                        middle_row = (start_row + end_row) // 2
                        middle_col = (start_col + end_col) // 2
                        middle_piece = self._grid[middle_row][middle_col]
                        if isinstance(middle_piece, checkers_piece):
                                self._grid[middle_row][middle_col] = '.'
                                if middle_piece._team == 'red':
                                    self._red_count -= 1
                                elif middle_piece._team == 'black':
                                    self._black_count -= 1

                        if (piece_to_move._team == 'red' and end_row == 7) or (piece_to_move._team == 'black' and end_row == 0):
                            piece_to_move.make_king()
                        
                        self.print_board()
                        return True
        return False

    def check_win(self):
        if self._red_count == 0:
            return "black"
        if self._black_count == 0:
            return "red"
        
        return False
