from buttons import *
from engine import *

gui_engine = GameEngine(1, 1, 10)

CURSOR = Back.RESET + Fore.YELLOW + '-> '
MENU_LINES_NUM = 17

cursor_index = 0

selected_game_size = (5, 5)
selected_snake_speed = 400

gui_run_flag = True


def onUpBtnClick():
    global cursor_index
    cursor_index = cursor_index - 1
    if cursor_index < 0:
        cursor_index += MENU_LINES_NUM

    if cursor_index == 1 or cursor_index == 8 or cursor_index ==15:
        cursor_index = (cursor_index - 1) % MENU_LINES_NUM


def onDownBtnClick():
    global cursor_index
    cursor_index = cursor_index + 1
    if cursor_index >= MENU_LINES_NUM:
        cursor_index -= MENU_LINES_NUM

    if cursor_index == 1 or cursor_index == 8 or cursor_index ==15:
        cursor_index = (cursor_index + 1) % MENU_LINES_NUM


def onEnterBtnClick():
    global cursor_index, selected_game_size, gui_run_flag, selected_snake_speed
    if cursor_index == 0:
        gui_run_flag = False
    elif 3 <= cursor_index <= 7:
        game_dim = (cursor_index - 2) * 5
        selected_game_size = (game_dim, game_dim)
    elif 10 <= cursor_index <= 14:
        selected_snake_speed = 200 * (cursor_index - 9)
    elif cursor_index == 16:
        exit(0)


def onESCBtnClick():
    exit(0)


def head_text_callback():
    global cursor_index, selected_game_size, selected_snake_speed
    menu_li = [
        Fore.CYAN + 'Start Game',
        Back.RESET + Fore.YELLOW + ' ',
        Back.RESET + Fore.CYAN + 'Select Map Size:',
        '  5  * 5',
        '  10 * 10',
        '  15 * 15',
        '  20 * 20',
        '  25 * 25',
        Back.RESET + Fore.YELLOW + ' ',
        Back.RESET + Fore.CYAN + 'Select Snake Speed:',
        '  200  ms',
        '  400  ms',
        '  600  ms',
        '  800  ms',
        '  1000 ms',
        Back.RESET + Fore.YELLOW + ' ',
        Back.RESET + Fore.CYAN + 'Exit',
    ]
    # put map size colors
    for i in range(3, 7 + 1):
        color = Back.RESET + Fore.MAGENTA if (selected_game_size[0] / 5 != i - 2) else Back.RESET + Fore.GREEN
        menu_li[i] = color + menu_li[i]

        # put snake speed colors
    for i in range(10, 14 + 1):
        color = Back.RESET + Fore.MAGENTA if (selected_snake_speed != 200 * (i - 9)) else Back.RESET + Fore.GREEN
        menu_li[i] = color + menu_li[i]

    # put cursor
    menu_li[cursor_index] = CURSOR + menu_li[cursor_index]

    return '\n'.join(menu_li)


def gui_screen():
    global selected_game_size, selected_snake_speed

    gui_engine.change_empty_cell(' ')
    gui_engine.clear_window()

    up_btn = BtnControl('up', BtnTrigger.OnPressTrigger, onUpBtnClick)
    down_btn = BtnControl('down', BtnTrigger.OnPressTrigger, onDownBtnClick)
    enter_btn = BtnControl('enter', BtnTrigger.OnPressTrigger, onEnterBtnClick)
    space_btn = BtnControl('space', BtnTrigger.OnPressTrigger, onEnterBtnClick)
    esc_btn = BtnControl('esc', BtnTrigger.OnPressTrigger, onESCBtnClick)

    gui_engine.add_control(up_btn)
    gui_engine.add_control(down_btn)
    gui_engine.add_control(enter_btn)
    gui_engine.add_control(space_btn)
    gui_engine.add_control(esc_btn)

    gui_engine.set_heading_text_callback(head_text_callback)

    while gui_run_flag:
        gui_engine.update_frame()
        gui_engine.update_tasks()
        gui_engine.check_buttons()

    return selected_game_size,selected_snake_speed
