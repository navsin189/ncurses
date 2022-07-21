#!/usr/bin/python3

import os
import sys
import curses
from curses.textpad import Textbox,rectangle

def input_file():
    """
    check which file needs to be edited
    """
    try:
        filename = sys.argv[1]
    except:
        print("no file provided")
        help = """
        notepad.py - text editor created in python
        Usage: ./notepad.py [file]
        """
        print(help)
        exit()
    
    screen(filename)

def screen(filename):
    """
    creating screen and launching editor
    """
    screen = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.noecho()

    begin_x = 30; begin_y = 2
    height = 25; width = 50
    try:
        win = curses.newwin(height, width, begin_y, begin_x)
        # rectangle(win, starting-y,starting-x, ending-y,ending-x )
        # rectangle(win, begin_y-1,begin_x-1, begin_y+height+1,begin_x+width+1 )
        screen.addstr(0,30,f"Curse Text Editor",curses.color_pair(1))
        screen.addstr(2,0,f"FileName -> {filename}",curses.color_pair(2))
        screen.addstr(5,0,"EXIT -> ctrl+G",curses.color_pair(3))
        for breadth in range(begin_x,begin_x+width):
            screen.addstr(begin_y-1,breadth,"-")
            screen.addstr(begin_y+height,breadth,"-")
        for length in range(begin_y,begin_y+height):
            screen.addstr(length,begin_x-1,"|")
            screen.addstr(length,begin_x+width,"|")

        screen.refresh()
        box = Textbox(win, True)
        box.edit()
        msg = box.gather()

        screen.addstr(begin_y+height+1,0,"saving...")
        screen.refresh()
        curses.napms(1000)
        curses.endwin()

        print("Saved...")
        # print(msg)

        with open(filename,"w") as edit:
            edit.write(msg)
    except:
        # curses.napms(1000)
        curses.endwin()
        print("not able to open editor")
        exit()

if __name__ == "__main__":
    """
    entry point for the script
    """
    input_file()