import random
import time

from buttons import *
from engine import *
from game_objects import *

WINDOW_WIDTH = 15
WINDOW_HEIGHT = 15
FPS = 30
SNAKE_MOVE_TIME_MILLI = 100
MAX_NUM_APPLES_IN_MAP = 3
MAX_NUM_BARRIERS_IN_MAP = 4

game_over = False
score = 0
game_start_time_seconds = time.time()

game_engine = None

snake = Snake([Position(i + 1, 1) for i in range(3)])
apples_list = []
barriers_list = []

snake_direction = 'right'


def onUpBtnClick():
    global snake_direction
    if snake_direction != 'down':
        snake_direction = 'up'


def onDownBtnClick():
    global snake_direction
    if snake_direction != 'up':
        snake_direction = 'down'


def onRightBtnClick():
    global snake_direction
    if snake_direction != 'left':
        snake_direction = 'right'


def onLeftBtnClick():
    global snake_direction
    if snake_direction != 'right':
        snake_direction = 'left'


def onESCBtnClick():
    print(Fore.RESET)
    exit(0)


def head_text_callback():
    global score, game_start_time_seconds

    game_time_seconds = int(time.time() - game_start_time_seconds)

    return '\n'.join([
        f"{Fore.BLUE}"
        f"Score: {score:4d}\t Time: {game_time_seconds:4d} s",
    ])


def snake_move():
    global snake_direction, snake, MAX_NUM_APPLES_IN_MAP, apples_list, game_over, score

    # snake movement
    if snake_direction == 'up':
        tail = snake.move_up(WINDOW_WIDTH, WINDOW_HEIGHT)
    elif snake_direction == 'down':
        tail = snake.move_down(WINDOW_WIDTH, WINDOW_HEIGHT)
    elif snake_direction == 'right':
        tail = snake.move_right(WINDOW_WIDTH, WINDOW_HEIGHT)
    elif snake_direction == 'left':
        tail = snake.move_left(WINDOW_WIDTH, WINDOW_HEIGHT)
    else:
        raise f"snake_direction {snake_direction} unsupported"

    # apples snake collision
    for snake_pos in snake.position_list:
        for j, apple in enumerate(apples_list):
            if apple.position == snake_pos:
                # dont remove tail of snake
                snake.position_list.insert(0, tail)
                apples_list.pop(j)
                score += 1
                break

    # barrier snake collision
    for snake_pos in snake.position_list:
        for barrier in barriers_list:
            if barrier.position == snake_pos:
                game_over = True
                break

    # snake-snake collision
    for i in range(len(snake.position_list)):
        for j in range(i + 1, len(snake.position_list)):
            if snake.position_list[i] == snake.position_list[j]:
                game_over = True

    # apples generator
    if len(apples_list) < MAX_NUM_APPLES_IN_MAP:
        new_apples_pos = random.choice(game_engine.get_all_empty_positions())
        apples_list.append(Apple(new_apples_pos))

    # barrier generator
    if len(barriers_list) < MAX_NUM_BARRIERS_IN_MAP:
        new_barriers_pos = random.choices(
            game_engine.get_all_empty_positions(),
            k=MAX_NUM_BARRIERS_IN_MAP - len(barriers_list))

        new_barriers = list(map(lambda pos: Barrier(pos), new_barriers_pos))
        barriers_list.extend(new_barriers)

    # adjust next frame
    game_engine.clear_window()
    for snake_pos in snake.position_list:
        game_engine.plot_symbol(snake_pos, str(snake))

    for apple in apples_list:
        game_engine.plot_symbol(apple.position, str(apple))

    for barrier in barriers_list:
        game_engine.plot_symbol(barrier.position, str(barrier))


def game_screen(window_width, window_height, snake_speed_ms):
    global WINDOW_WIDTH, WINDOW_HEIGHT, game_engine, SNAKE_MOVE_TIME_MILLI, game_start_time_seconds

    game_start_time_seconds = time.time()

    WINDOW_WIDTH = window_width
    WINDOW_HEIGHT = window_height
    SNAKE_MOVE_TIME_MILLI = snake_speed_ms

    game_engine = GameEngine(WINDOW_WIDTH, WINDOW_HEIGHT, FPS)

    up_btn = BtnControl('up', BtnTrigger.OnPressTrigger, onUpBtnClick)
    down_btn = BtnControl('down', BtnTrigger.OnPressTrigger, onDownBtnClick)
    right_btn = BtnControl('right', BtnTrigger.OnPressTrigger, onRightBtnClick)
    left_btn = BtnControl('left', BtnTrigger.OnPressTrigger, onLeftBtnClick)
    esc_btn = BtnControl('esc', BtnTrigger.OnPressTrigger, onESCBtnClick)

    game_engine.add_control(up_btn)
    game_engine.add_control(down_btn)
    game_engine.add_control(right_btn)
    game_engine.add_control(left_btn)
    game_engine.add_control(esc_btn)

    game_engine.add_task(PeriodicTask(snake_move, SNAKE_MOVE_TIME_MILLI))

    game_engine.set_heading_text_callback(head_text_callback)

    while not game_over:
        game_engine.update_frame()
        game_engine.check_buttons()
        game_engine.update_tasks()

    print(Back.RESET + Fore.RED + 'Game Over')
