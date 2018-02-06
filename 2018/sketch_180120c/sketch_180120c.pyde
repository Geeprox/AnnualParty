# R: Close auto choose
# H: Hey
# J: Close hey
# C: Completely random
# V: Close Completely random

import os
import json
import random as origin_random

CONFIG_FILEPATH = 'cfg.json'
FOCUSE_RADIUS = 100
INIT_FONT_SIZE = 14
MULTIPLE = 2
INIT_FONT_COLOR = 120
INIT_LINE_COLOR = 160
MAX_FONT_COLOR = 0
RANDOM_STEP = 0.5
FONT = 'inziu-SC-regular.ttf'
FONT_BOLD = 'inziu-SC-bold.ttf'
BACKGROUND = 255

config = {}
charnodes = []
draw_nodes = []

auto_choosing = False
auto_choosing_found = False
auto_direction = (RANDOM_STEP, RANDOM_STEP)

completely_random = False

hey = True
plan_index = 0
matched_plans = []

cur_frame_index = 0
CHOICE_PER_N_FRAME = 2
this_choice = '???'
completely_random_is_pausing = True

names_pool = []
except_pool = set()

class CharNode:
    def __init__(self, value, xy):
        self.value = value
        self.init_pos = xy

    def update(self):
        x, y = self.init_pos

        global auto_choosing, cursor_x, cursor_y, auto_direction, hey, matched_plans, plan_index
        dir_x, dir_y = auto_direction

        if auto_choosing:
            if auto_choosing_found:
                if not matched_plans:
                    hey = False

                if hey and plan_index < len(matched_plans):
                    matched_one = matched_plans[plan_index]
                    matched_one = matched_one[0] + '  ' + matched_one[1] if len(matched_one) == 2 else matched_one
                else:
                    hey = False

                min_dis = width * width
                matched_xy = (0, 0)
                for node in charnodes:
                    if not hey or node.value == matched_one:
                        temp_dis = pow(cursor_x - node.init_pos[0], 2) + pow(cursor_y - node.init_pos[1], 2)
                        if temp_dis < min_dis:
                            matched_xy = node.init_pos
                            min_dis = temp_dis

                cursor_x += abs(RANDOM_STEP) / 2 if matched_xy[0] > cursor_x else -abs(RANDOM_STEP) / 2
                cursor_y += abs(RANDOM_STEP) / 2 if matched_xy[1] > cursor_y else -abs(RANDOM_STEP) / 2
            else:
                delta_x = dir_x if random(0, 1) > 0.4 else -dir_x
                cursor_x += delta_x
                delta_y = dir_y if random(0, 1) > 0.4 else -dir_y
                cursor_y += delta_y

                if cursor_x < start_x or cursor_x > block_width:
                    cursor_x -= delta_x * 2
                    dir_x = -dir_x
                if cursor_y < start_y or cursor_y > block_height:
                    cursor_y -= delta_y * 2
                    dir_y = -dir_y

                auto_direction = (dir_x, dir_y)
        else:
            cursor_x = mouseX
            cursor_y = mouseY

        dis_x = x - cursor_x
        dis_y = y - cursor_y

        dis = sqrt(dis_x * dis_x + dis_y * dis_y)

        ratio = 0
        MULTIPLE = 2

        if dis < FOCUSE_RADIUS:
            disp = 1 + cos(PI * dis / FOCUSE_RADIUS)
            now_pos_x = x + MULTIPLE * dis_x * disp / 2
            now_pos_y = y + MULTIPLE * dis_y * disp / 2
            ratio = MULTIPLE * (1 - sin(PI * (dis / FOCUSE_RADIUS) / 2))

            stroke(INIT_LINE_COLOR)
            line(x, y, now_pos_x, now_pos_y)
        else:
            now_pos_x, now_pos_y = self.init_pos

        now_size = INIT_FONT_SIZE * (ratio + 1)
        now_color = INIT_FONT_COLOR + ratio * \
            (MAX_FONT_COLOR - INIT_FONT_COLOR)

        fill(INIT_LINE_COLOR)
        line(x, y, now_pos_x, now_pos_y)

        draw_nodes.append((now_size, now_color, self.value, now_pos_x, now_pos_y))

def setup():
    fullScreen()
    smooth()
    # frameRate(30)
    textAlign(CENTER, CENTER)

    with open(CONFIG_FILEPATH, 'rt') as f:
        global config
        config = json.load(f)

    global cursor_x, cursor_y, names_pool
    cursor_x, cursor_y = width / 2, height / 2

    this_font = createFont(FONT, INIT_FONT_SIZE * 10, True)
    textFont(this_font)

    names = config.get('all')
    origin_random.shuffle(names)
    names_pool = names

    names *= 5
    names_num = len(names)

    width_num = int(sqrt(names_num) + 0.5)
    height_num = int(names_num / width_num + 0.5)

    textSize(INIT_FONT_SIZE)
    double_char_width = int(textWidth('TEST') / 2)

    charnode_width = double_char_width * 4

    global start_x, start_y, block_width, block_height
    start_x = int(width / 2) - charnode_width * int(width_num / 2 + 1)
    start_y = int(height / 2) - height_num * double_char_width
    block_width = width - start_x
    block_height = height - start_y

    for index, name in enumerate(names):
        x = start_x + index % width_num * (charnode_width + double_char_width / 2)
        y = start_y + int(index / width_num) * double_char_width * 2
        formated_name = name[0] + '  ' + name[1] if len(name) == 2 else name
        charnode = CharNode(formated_name, (x, y))

        charnodes.append(charnode)


def mousePressed():
    global focusing, auto_choosing, auto_choosing_found, plan_index, hey, completely_random_is_pausing

    if completely_random:
        if not completely_random_is_pausing:
            completely_random_is_pausing = True
            except_pool.add(this_choice)
        else:
            completely_random_is_pausing = False

        return

    if auto_choosing:
        if not auto_choosing_found:
            auto_choosing_found = True
            focusing = True
            if mouseY > height / 2:
                hey = True
            else:
                hey = False
        else:
            auto_choosing_found = False
            if hey:
                plan_index += 1
    else:
        if mouseButton == LEFT:
            focusing = True
        else:
            global cursor_x, cursor_y
            cursor_x, cursor_y = width / 2, height / 2
            auto_choosing = True


def mouseReleased():
    global focusing, auto_choosing, auto_choosing_found

    if not auto_choosing:
        focusing = False


def keyPressed():
    global auto_choosing, hey, completely_random, this_choice

    if key in ['r', 'R']:
        auto_choosing = False
    elif key in ['h', 'H']:
        hey = True
    elif key in ['j', 'J']:
        hey = False
    elif key in ['c', 'C']:
        completely_random = True
    elif key in ['v', 'V']:
        completely_random = False
        this_choice = '???'
    elif key in [str(i) for i in range(10)]:
        global matched_plans, plan_index, auto_choosing_found

        if auto_choosing_found:
            return

        matched_plans = config.get('hey_plan').get(key)
        plan_index = 0

        print('Plan:', key)

        if matched_plans is None:
            hey = False
            print('Unknown plan')
        else:
            hey = True


def update_draw_nodes():
    global draw_nodes
    draw_nodes = []

    for char_node in charnodes:
        char_node.update()

    draw_nodes.sort(key=lambda x: x[0])

    for node in draw_nodes:
        now_size, now_color, value, now_pos_x, now_pos_y = node

        textSize(now_size)
        fill(now_color)
        text(value, now_pos_x, now_pos_y)


def update_completely_random_names():
    global cur_frame_index, CHOICE_PER_N_FRAME, this_choice, names_pool, except_pool

    if not completely_random_is_pausing:
        if cur_frame_index > CHOICE_PER_N_FRAME:
            while True:
                this_choice = origin_random.choice(names_pool)
                if this_choice not in except_pool:
                    break

            cur_frame_index = 0

        cur_frame_index += 1

    textSize(70)
    fill(0)
    text(this_choice, width / 2, height / 2)


def draw():
    background(BACKGROUND)

    if completely_random:
        update_completely_random_names()
    else:
        update_draw_nodes()