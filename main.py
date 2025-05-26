from game_screen import *
from gui_screen import *


def main():
    selected_game_size, selected_snake_speed = gui_screen()

    game_screen(*selected_game_size, selected_snake_speed)


if __name__ == "__main__":
    main()
