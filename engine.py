import os
import time

from colorama import Fore, Back

from buttons import BtnControl
from utilities import Position



class PeriodicTask:
    def __init__(self, callback, time_period_ms):
        self.callback = callback
        self.time_period_ms = time_period_ms

        self.last_call_time_ns = None



    def check(self):
        if self.last_call_time_ns is None or time.time_ns() > self.last_call_time_ns + self.time_period_ms * (10 ** 6):
            self.last_call_time_ns = time.time_ns()
            return True
        return False


class GameEngine:
    def __init__(self, window_width, window_height, fps):
        assert type(window_width) is int and type(window_width) is int
        assert type(fps) is int

        #empty cell
        self.empty_cell = Back.RESET + Fore.LIGHTWHITE_EX + '-'

        self.window_width = window_width
        self.window_height = window_height
        self.fps = fps

        # create window
        self.window = []
        for i in range(window_height):
            self.window.append([])
            for j in range(window_width):
                self.window[-1].append(self.empty_cell)

        # fps variables
        self.last_frame_time = None

        # buttons
        self.buttons = []

        # periodic tasks
        self.tasks = []

        # heading text
        self.heading_text_callback = None




    def window_to_str(self):
        window_str = ""

        for i in range(self.window_height):
            for j in range(self.window_width):
                window_str += str(self.window[i][j])
                window_str += Back.RESET + ' '

            window_str += '\n'

        window_str = window_str.strip()

        return window_str

    def add_control(self, btn: BtnControl):
        assert type(btn) is BtnControl

        self.buttons.append(btn)

    def add_task(self, task: PeriodicTask):
        assert type(task) is PeriodicTask

        self.tasks.append(task)

    def update_frame(self):
        period_time_ns = (1 / self.fps) * 10 ** 9

        if self.last_frame_time is None or time.time_ns() >= self.last_frame_time + period_time_ns:
            # update time
            self.last_frame_time = time.time_ns()

            # plot new frame and clear old one
            os.system('cls')

            frame_str = self.window_to_str()

            if self.heading_text_callback is not None:
                frame_str = str(self.heading_text_callback()) + '\n' + frame_str

            print(frame_str)

    def update_tasks(self):
        for task in self.tasks:
            if task.check():
                task.callback()

    def check_buttons(self):
        for btn in self.buttons:
            if btn.check():
                btn.callback()

    def clear_window(self):
        for i in range(self.window_height):
            for j in range(self.window_width):
                self.window[i][j] = self.empty_cell

    def plot_symbol(self, position: Position, symbol):
        assert type(position) is Position and type(symbol) is str
        assert position.x < self.window_width
        assert position.y < self.window_height

        self.window[position.y][position.x] = symbol

    def clear_at(self, position: Position):
        assert type(position) is Position
        assert position.x < self.window_width
        assert position.y < self.window_height

        self.window[position.y][position.x] = self.empty_cell

    def get_all_empty_positions(self):
        empty_pos = []

        for i in range(self.window_height):
            for j in range(self.window_width):
                if self.window[i][j] == self.empty_cell:
                    empty_pos.append(
                        Position(j, i)
                    )

        return empty_pos

    def set_heading_text_callback(self, callback):
        self.heading_text_callback = callback

    def change_empty_cell(self, digit):
        self.empty_cell = Back.RESET + Fore.LIGHTWHITE_EX + str(digit)[0]
