#!/usr/bin/python3

import os
import sys
import curses
from curses.textpad import Textbox

def input_file():
    """
    check which file needs to be edited
    """
    filename = sys.argv[1]
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
    height = 20; width = 60
    win = curses.newwin(height, width, begin_y, begin_x)

    screen.addstr(0,0,f"FileName -> {filename}")
    screen.addstr(1,0,"EXIT -> ctrl+G")
    screen.refresh()
    box = Textbox(win)
    box.edit()
    msg = box.gather()

    screen.addstr(height+1,0,"saving...")
    screen.refresh()
    curses.napms(1000)
    curses.endwin()

    print("Saved...")
    print(msg)

    with open(filename,"w") as edit:
        edit.write(msg)

if __name__ == "__main__":
    """
    entry point for the script
    """
    input_file()