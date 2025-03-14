from lan_checkers import lan_checkers_game
from websockets_checkers import websockets_checkers_game
def main():
    while True:
        lan_or_web = input("input (1) for lan or (2) for web: ")
        if lan_or_web == '1':
            game = lan_checkers_game()
            game.main_loop()

        elif lan_or_web == '2':
            game = websockets_checkers_game()
            game.main_loop()

if __name__ == "__main__":
    main()