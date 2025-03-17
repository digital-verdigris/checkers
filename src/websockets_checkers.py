import asyncio
import pygame
import threading
import json
from board import checkers_board
from menu import checkers_menu
from websockets_client import checkers_websockets_client  
from websockets_server import checkers_websockets_server

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = 512 // 8

class websockets_checkers_game:
    def __init__(self):
        self.game_board = checkers_board()
        self.menu = checkers_menu()
        self.clock = pygame.time.Clock()
        self.turn = 'black'
        self.channel_open = False
        
        # Initialize pygame
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Verdigris Checkers")

        self.running = True
        self.team = None
        self.client = None

    def change_turn(self):
        # Switch turn and update the board state
        self.turn = 'red' if self.turn == 'black' else 'black'
        self.game_board._turn = self.turn
        self.game_board.update_valid_pieces()

    def send_move(self, move):
        # Update the board with the move.
        self.game_board.move_piece(move)
        # Send the move over WebRTC as a JSON message if the data channel is ready.
        if self.client and self.client.channel and self.client.channel.readyState == "open":
            print(f"Sent move: {move}")
            self.client.send_move(move)
        self.change_turn()

    def receive_move(self, move):
        self.game_board.move_piece(move)
        self.change_turn()

    def notify_data_channel_opened(self):
        self.channel_open = True

    def start_signaling_server(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(checkers_websockets_server().start())

    def run_async_client(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.client.connect_signaling())

    def main_loop(self):
        menu_response = self.menu.main_menu(self.window)
    
        password = self.menu.draw_input_password(self.window)
        if password is None:
            self.close()
            return

        if menu_response == 'h':
            self.team = 'black'
            self.game_board._team = 'black'

            # Create a WebRTC client as the "offer" for hosting.
            self.client = checkers_websockets_client("offer", "wss://localhost:5000", self, password)
            threading.Thread(target=self.run_async_client, daemon=True).start()
    
        elif menu_response == 'c':
            self.team = 'red'
            self.game_board._team = 'red'
            # Create a WebRTC client as the "answer" for joining.
            self.client = checkers_websockets_client("answer", "wss://localhost:5000", self, password)
            threading.Thread(target=self.run_async_client, daemon=True).start()

        else:
            self.close()


        while not self.channel_open:
            self.menu.draw_waiting_menu(self.window)
            pygame.display.update()
            self.clock.tick(30)

        self.game_loop()

    async def wait_for_connection(self):
        while not self.channel_open:
            self.menu.draw_waiting_menu(self.window)
            pygame.display.update()
            await asyncio.sleep(0.1)

    def game_loop(self):
        while self.running:
            self.clock.tick(60)  # 60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.turn == self.team:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        col = (mouse_x // SQUARE_SIZE) - 1
                        row = (mouse_y // SQUARE_SIZE) - 1
                        if (0 <= col <= 7) and (0 <= row <= 7):
                            if self.game_board._selected_piece is None:
                                self.game_board.select_piece(row, col)
                            else:
                                move = (self.game_board._selected_pos[0],
                                        self.game_board._selected_pos[1], row, col)
                                if self.game_board.validate_move(move):
                                    self.send_move(move)
                                self.game_board.deselect_piece()

            self.game_board.draw_board(self.window)
            pygame.display.update()

            winner = self.game_board.check_win()
            if winner:
                self.running = False
        
        self.menu.draw_win_screen(self.window, winner)

        self.close()

    def close(self):
        if self.client:
            self.client.pc.close()
        pygame.quit()
