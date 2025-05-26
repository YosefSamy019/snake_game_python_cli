import time
from abc import ABC

from colorama import Fore, Back

from utilities import *


class GameObject(ABC):
    def __init__(self):
        pass


class Apple(GameObject):
    def __init__(self, position):
        super().__init__()
        assert type(position) is Position
        self.position = position

        self.create_time_ns = time.time_ns()

    def __str__(self):
        life_time_ns = time.time_ns() - self.create_time_ns
        create_time_s = life_time_ns // (10 ** 9)

        cur_color = [Fore.GREEN, Fore.YELLOW][create_time_s % 2]

        return Back.MAGENTA + cur_color + "\u047C"


class Snake(GameObject):
    def __init__(self, position_list):
        super().__init__()
        assert type(position_list) is list and type(position_list[0]) is Position
        self.position_list = position_list

    def __str__(self):
        return Back.RESET + Fore.YELLOW + "\u25A0"

    def move_up(self, screen_width, screen_height):
        tail = self.position_list.pop(0)
        head = self.position_list[-1]

        new_head = head + Position(0, -1)
        new_head.limit(screen_width, screen_height)

        self.position_list.append(new_head)
        return tail

    def move_down(self, screen_width, screen_height):
        tail = self.position_list.pop(0)
        head = self.position_list[-1]

        new_head = head + Position(0, 1)
        new_head.limit(screen_width, screen_height)

        self.position_list.append(new_head)
        return tail

    def move_right(self, screen_width, screen_height):
        tail = self.position_list.pop(0)
        head = self.position_list[-1]

        new_head = head + Position(1, 0)
        new_head.limit(screen_width, screen_height)

        self.position_list.append(new_head)
        return tail

    def move_left(self, screen_width, screen_height):
        tail = self.position_list.pop(0)
        head = self.position_list[-1]

        new_head = head + Position(-1, 0)
        new_head.limit(screen_width, screen_height)

        self.position_list.append(new_head)
        return tail


class Barrier(GameObject):
    def __init__(self, position):
        super().__init__()
        assert type(position) is Position
        self.position = position

    def __str__(self):
        return Back.RESET + Fore.RED + "X"
