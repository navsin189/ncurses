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
    # try:
    #     filename = sys.argv[1]
    #     filename = str(filename)
    #     screen(filename)
    # except:
    #     print("no file provided, terminating")
    #     exit()

def screen(filename):
    """
    creating screen and launching editor
    """
    screen = curses.initscr()
    curses.noecho()

    begin_x = 30; begin_y = 1
    height = 10; width = 20
    try:
        win = curses.newwin(height, width, begin_y, begin_x)
        # rectangle(win, starting-y,starting-x, ending-y,ending-x )
        # rectangle(win, begin_y-1,begin_x-1, begin_y+height+1,begin_x+width+1 )
        screen.addstr(0,0,f"FileName -> {filename}")
        screen.addstr(1,0,"EXIT -> ctrl+G")
        screen.refresh()
        box = Textbox(win, True)
        box.edit()
        msg = box.gather()

        screen.addstr(height+1,0,"saving...")
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