from colorama import Fore

from utilities import *


class Apple:
    def __init__(self, position):
        assert type(position) is Position
        self.position = position

    def __str__(self):
        return Fore.GREEN + "\u047C"


class Snake:
    def __init__(self, position_list):
        assert type(position_list) is list and type(position_list[0]) is Position
        self.position_list = position_list

    def __str__(self):
        return Fore.YELLOW + "\u25A0"

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


class Barrier:
    def __init__(self, position):
        assert type(position) is Position
        self.position = position

    def __str__(self):
        return Fore.RED + "X"
