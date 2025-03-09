import pygame

#constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8,8
SQUARE_SIZE = 512 // 8

#button constants
button_width, button_height = 200, 50
start_host_button = pygame.Rect((WIDTH // 2 - button_width // 2, 100), (button_width, button_height))
start_connect_button = pygame.Rect((WIDTH // 2 - button_width // 2, 200), (button_width, button_height))
quit_button = pygame.Rect((WIDTH // 2 - button_width // 2, 300), (button_width, button_height))

#colors
WHITE = (255,255,255)
GRAY  = (150,150,150)
BLACK = (0,0,0)
RED   = (255,0,0)
GREEN = (55,148,110)
BLUE  = (0,0,255)
BROWN = (69,40,60)

pygame.font.init()
font = pygame.font.Font(None, 50)

class checkers_menu:
    def __init__(self):
        self.felt_img = pygame.image.load("assets/textures/felt_texture.jpg")
        self.felt_img = pygame.transform.scale(self.felt_img, (WIDTH, HEIGHT))
        self.input_text = ""
        self.active_input = False 

    def draw_lan_or_web(self, window):
        window.fill(GREEN)
        window.blit(self.felt_img, (0, 0))

    def draw_menu(self, window):
        window.fill(GREEN)
        window.blit(self.felt_img, (0, 0))

        pygame.draw.rect(window, GRAY, start_host_button)
        pygame.draw.rect(window, GRAY, start_connect_button)
        pygame.draw.rect(window, GRAY, quit_button)
        
        start_host_text = font.render("Black", True, BLACK)
        start_connect_text = font.render("Red", True, RED)
        quit_text = font.render("Quit", True, BLACK)
        
        window.blit(start_host_text, (start_host_button.x + 55, start_host_button.y + 10))
        window.blit(start_connect_text, (start_connect_button.x + 65, start_connect_button.y + 10))
        window.blit(quit_text, (quit_button.x + 60, quit_button.y + 10))
       
        pygame.display.update()

    def draw_waiting_menu(self, window):
        window.blit(self.felt_img, (0, 0))
        ip_text = font.render("Waiting For Connection...", True, BLACK)
        window.blit(ip_text, (150, HEIGHT // 4))

    def draw_waiting_for_connection(self, window, host_ip):
        window.blit(self.felt_img, (0, 0))
        
        ip_text = font.render(f"Hosting At: {host_ip}...", True, BLACK)
        window.blit(ip_text, (150, HEIGHT // 4))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        pygame.display.update()
        return True

    def draw_win_screen(self, window, winner):
        while True:
            window.blit(self.felt_img, (0, 0))
            winner_text = None
            
            if winner == 'black':
                winner_text = font.render(f"Black Wins!", True, BLACK)
            elif winner == 'red':
                winner_text = font.render(f"Red Wins!", True, RED)
        
            window.blit(winner_text, (150, HEIGHT // 4))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False 

    def draw_input_password(self, window):
        while True:
            window.blit(self.felt_img, (0, 0))

            ip_text = font.render("Enter Password...", True, BLACK)
            window.blit(ip_text, (120, HEIGHT // 4))
            
            input_box = pygame.Rect(120, HEIGHT // 4 + 50, 400, 50)
            pygame.draw.rect(window, GRAY, input_box) 

            input_text = font.render(self.input_text, True, BLACK)
            window.blit(input_text, (input_box.x + 10, input_box.y + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if self.active_input:
                        if event.key == pygame.K_RETURN:
                            return self.input_text
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            self.input_text += event.unicode 

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        self.active_input = True 
                    else:
                        self.active_input = False

            pygame.display.update()
        return None

    def main_menu(self, window):
        running = True
        while running:
            self.draw_menu(window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_host_button.collidepoint(event.pos):
                        running = False
                        return 'h'
                    elif start_connect_button.collidepoint(event.pos):
                        running = False
                        return 'c'
                    elif quit_button.collidepoint(event.pos):
                        return False
        return False
