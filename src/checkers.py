import pygame
import threading
from server import checkers_server
from client import checkers_client
from board import checkers_board
from menu import checkers_menu
from keygen import checkers_keygen

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8,8
SQUARE_SIZE = 512 // 8

class checkers_game:
    def __init__(self):
        self.game_board = checkers_board()
        self.menu = checkers_menu()
        self.clock = pygame.time.Clock()
        self.turn = 'black'
        
        #pygame initialization
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("verdigris checkers")

        self.running = True

    def change_turn(self):
        if self.turn == 'black':
            self.turn = 'red'
            self.game_board._turn = self.turn
            self.game_board.update_valid_pieces()
            
        elif self.turn == 'red':
            self.turn = 'black'
            self.game_board._turn = self.turn
            self.game_board.update_valid_pieces()

    def send_move(self, move):
        self.game_board.move_piece(move)

        if hasattr(self, 'client'):
            self.client.send_move(str(move))
            self.change_turn()

        elif hasattr(self, 'server'):
            self.server.send_move(str(move))
            self.change_turn()

    def recieve_move(self):
        if hasattr(self, 'client') and self.turn == 'black':
            move = self.client.receive_move()
            if move:
                self.game_board.move_piece(eval(move))
                self.change_turn()

        elif hasattr(self, 'server') and self.turn == 'red':
            move = self.server.receive_move()
            if move:
                self.game_board.move_piece(eval(move))
                self.change_turn()

    def validate_move(self, move):
        return self.game_board.validate_move(move)

    def main_loop(self):
        menu_response = self.menu.main_menu(self.window)
    
        if menu_response == 'h':
            keygen = checkers_keygen("server")
            keygen.generate_keys_and_certificate()

            self.team = 'black'
            self.game_board._team = 'black'
            self.server = checkers_server()
            threading.Thread(target=self.server.start_listener, daemon=True).start()
            if self.server.wait_for_client(self.menu, self.window):
                self.game_loop()
            else:
                self.close()

        elif menu_response == 'c':
            keygen = checkers_keygen("client")
            keygen.generate_keys_and_certificate()

            self.team = 'red'
            self.game_board._team = 'red'
            self.client = checkers_client()
            self.client.connect_to_server()
            self.game_loop()

        else:
            self.close()

    def game_loop(self):
        while self.running:
            self.clock.tick(60)  #60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
                if self.turn == self.team:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos

                        col = (mouse_x // SQUARE_SIZE) - 1
                        row = (mouse_y // SQUARE_SIZE) - 1

                        if (col >= 0 and col <= 7) and (row >= 0 and row <= 7):
                            if self.game_board._selected_piece is None:
                                self.game_board.select_piece(row, col)
                            else:
                                move = (self.game_board._selected_pos[0],self.game_board._selected_pos[1], row, col)

                                if self.validate_move(move):
                                    self.send_move(move)
                                self.game_board.deselect_piece()
                else:
                    self.recieve_move()

            self.game_board.draw_board(self.window)            
            pygame.display.update()

            if self.game_board.check_win():
                self.running = False
        
        self.close()

    def close(self):
        if hasattr(self, 'server'):
            self.server.close()

        elif hasattr(self, 'client'):
            self.client.close()

        pygame.quit()

def main():
    game = checkers_game()
    game.main_loop()

if __name__ == "__main__":
    main()