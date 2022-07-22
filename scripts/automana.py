import pywinauto
# import pandas as pd
# import numpy as np
# import os
# import cv2 as cv
import mouse

# import time
from collections import deque
import itertools as itt
from pynput import keyboard

import threading

# import ctypes
# user32 = ctypes.windll.user32
# screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def clicker(is_child=False):
    global RUNNING_FLAG
    RUNNING_FLAG = True

    if not input_queues: 
        return None
    # print(input_queues)
    key = input_queues.popleft()
    if key == ']':
        exit()
    if key == '`':
        clicks()
    if key == 'f2':
        mid_click()
    if key == 'f4':
        deep_clicks()
    
    if input_queues:
        clicker(is_child=True)

    if not is_child:
        RUNNING_FLAG = False

def on_press(key):
    global RUNNING_FLAG
    
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == ']':
        exit()
    if k not in ['`', 'f2']:
        return None

    if len(input_queues) < 2:
        input_queues.append(k)

    if RUNNING_FLAG == False:
        RUNNING_FLAG = True
        t1 = threading.Thread(target=clicker)
        t1.start()
    
    try:
        print('Key pressed: ' + k)
    except:
        pass

def pair_iter(pos):
    first = deque(pos)
    second = deque(pos)
    second.rotate()
    return list(zip(first, second))

def scale(positions, rect):
    # Rectangle has padding of 8
    r, l = rect.right - 8, rect.left + 8
    b, t = rect.bottom - 8, rect.top + 8

    W, H = 1936 - 16, 1056 - 16
    w, h = abs(r - l), abs(b - t)
    return [(int(x * w / W) + l, int(y * h / H) + t) for x, y in positions]

'''
1080p
'''
raw_pos = [(695, 745), (493, 515), (753, 398), (1045, 368), (1318, 440), (1438, 607), (1429, 614), (1261, 781), (929, 860)] #last is bottom, left to right is clock wise
# out_pos = [(953, 882), (533, 767), (458, 529), (717, 346), (1073, 325), (1340, 425), (1479, 600), (1334, 826)] #first is bottom
# in_pos = [(943, 774), (645, 676), (537, 517), (749, 418), (1015, 382), (1280, 454), (1378, 609), (1245, 735)]

'''
2k screen
'''
out_pos = [(1270, 1187), (710, 1032), (610, 712), (956, 465), (1430, 437), (1786, 572), (1972, 807), (1778, 1111)]
in_pos = [(1257, 1041), (860, 910), (716, 695), (998, 562), (1353, 514), (1706, 611), (1837, 819), (1660, 989)]
center_pos = (1288, 758)

def mid_click():
    mouse.move(*center_pos)
    mouse.click()

def clicks():
    for out_p, in_p in set_pos:
        mouse.move(*out_p)
        mouse.drag(*out_p, *in_p, duration=1e-10)

def deep_clicks():
    for a, b in itt.chain.from_iterable(itt.repeat(paired_iter, 2)):
        out_a, in_a = a
        out_b, in_b = b
        mouse.drag(*out_a, *in_a, duration=1e-10)
        mouse.drag(*in_a, *out_b, duration=1e-10)

def start_keyboard():
    print('Starting keyboard listener')
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    print('=== Ready ===')
    print('Press ` (grave accent) to circle the mouse once.')
    print('Press F2 to click center.')
    print('Press ] to exit.')
    print('[For Debug] Press F4 to circle with more coverage.')

    listener.join()  # remove if main thread is polling self.keys

def main():
    global input_queues
    global RUNNING_FLAG
    input_queues = deque()
    RUNNING_FLAG = False

    # t1 = threading.Thread(target=clicker)
    # t1.start()

    print('=== Started ===')
    
    # try:
    #     repeats = int(input('Repeats per click (1 or more) [1]: ') or '1')
    # except:
    #     repeats = 1
    # auto_scale = (input("Auto scale? (for screen less than 1080p or doesn't play on windowed maximize) \n(y/n) [n]: ") or 'n') == 'y'
    repeats = 1
    auto_scale = False
    print('2k version locked')

    global set_pos
    global paired_iter

    set_pos = list(zip(out_pos, in_pos))
    paired_iter = pair_iter(set_pos)
    set_pos = list(zip(out_pos, in_pos)) * repeats

    if auto_scale:
        app = pywinauto.Application('uia').connect(title_re='Assaultlily*')
        wndw = app.window()
        rect = wndw.rectangle()
        set_pos = list(zip(scale(out_pos, rect), scale(in_pos, rect)))
        print(scale(out_pos, rect))
        print(scale(in_pos, rect))
        paired_iter = pair_iter(set_pos)

    start_keyboard()
    

if __name__ == '__main__':
    main()
    