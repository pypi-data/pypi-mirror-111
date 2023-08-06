# -*- encoding: utf-8 -*-
"""
@File    : pickerUI.py
@Time    : 2021/7/1 5:18 下午
@Author  : Jiaoxuewei
@Email   : jovae@qq.com
"""

# 导入外部库
import sys
import termios
import tty

# 导入内部库


CREL_C = '\x03'
DIRECTIION_PREFIX = '\x1b'
UP = '\x1b[A'
DOWN = '\x1b[B'
ENTER = '\r'


def show_choose(choice_list, pos):
    i = 0
    s = ''
    while i < len(choice_list):
        if i == pos:
            temp = '\033[33;1m => '
        else:
            if choice_list[i]['disabled']:
                temp = ''
            else:
                temp = '    '
        temp += str(choice_list[i]['info']) + '\033[0m\n'
        i += 1
        s += temp
    s += '\n'
    sys.stdout.write(s)
    sys.stdout.flush()


def clear_choose(choice_list):
    sys.stdout.write('\033[%dA\033[K' % (len(choice_list) + 1,))
    sys.stdout.flush()


def get_input():
    ch = sys.stdin.read(1)
    if ch == DIRECTIION_PREFIX:
        ch += sys.stdin.read(2)
    return ch


def show_menu(choice_list, pos=0, is_first=True):
    if is_first:
        sys.stdout.flush()
    if not is_first:
        clear_choose(choice_list)
    show_choose(choice_list, pos)


def flatten(choice_info):
    choice_list = []
    for key in choice_info:
        choice_list.append({'info': key+":", 'disabled': True})
        for value in choice_info[key]:
            choice_list.append({'info': value, 'disabled': False, 'type': key})
    return choice_list


def pick(choice_info):
    choice_list = flatten(choice_info)

    pos = 0
    while choice_list[pos]['disabled'] == True:
        pos = (pos + 1) % len(choice_list)

    show_menu(choice_list, pos)

    while True:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = get_input()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if key == CREL_C:
            break
        elif key == ENTER:
            return choice_list[pos]['info'], choice_list[pos]['type']
        elif key == UP:
            pos = (pos - 1) % len(choice_list)
            while choice_list[pos]['disabled'] == True:
                pos = (pos - 1) % len(choice_list)
        elif key == DOWN:
            pos = (pos + 1) % len(choice_list)
            while choice_list[pos]['disabled'] == True:
                pos = (pos + 1) % len(choice_list)

        show_menu(choice_list, pos, False)


if __name__ == '__main__':
    from pickerUI import pick
    target, level = pick({"A":[0,1,2], "B":[0,1,2]})
    print(target, level)