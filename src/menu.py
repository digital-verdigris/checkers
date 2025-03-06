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
        pass

    def draw_menu(self, window):
        window.fill(GREEN)
        window.blit(self.felt_img, (0, 0))

        pygame.draw.rect(window, GRAY, start_host_button)
        pygame.draw.rect(window, GRAY, start_connect_button)
        pygame.draw.rect(window, GRAY, quit_button)
        
        start_host_text = font.render("Start Host", True, BLACK)
        start_connect_text = font.render("Connect To Host", True, BLACK)
        quit_text = font.render("Quit", True, BLACK)
        
        window.blit(start_host_text, (start_host_button.x + 50, start_host_button.y + 10))
        window.blit(start_connect_text, (start_connect_button.x + 50, start_connect_button.y + 10))
        window.blit(quit_text, (quit_button.x + 50, quit_button.y + 10))
        pygame.display.update()

    def draw_waiting_for_connection(self, window):
        window.blit(self.felt_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        pygame.display.update()
        return True

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
