#!/usr/bin/python3

import os
import sys
import curses
from curses.textpad import Textbox

def input_file():
    """
    check which file needs to be edited
    """
    try:
        filename = sys.argv[1] #takes first argument
    except:
        print("no file provided")
        help = """
        notepad.py - text editor created in python
        Usage: ./notepad.py [file]
        """
        print(help)
        exit()
    
    screen(filename) # calling screen function

def screen(filename):
    """
    creating screen and launching editor
    """
    screen = curses.initscr() #initialize new screen
    curses.start_color() #to use colored text
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE) #(assign a number, text color, background color)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.noecho()

    begin_x = 30; begin_y = 2
    height = 25; width = 50
    try:
        win = curses.newwin(height, width, begin_y, begin_x) #initializing new windiw on screen
        screen.addstr(0,30,f"Curse Text Editor",curses.color_pair(1)) #adding text on specified coordinate
        screen.addstr(2,0,f"FileName -> {filename}",curses.color_pair(2))
        screen.addstr(5,0,"EXIT -> ctrl+G",curses.color_pair(3))
        for breadth in range(begin_x,begin_x+width):
            screen.addstr(begin_y-1,breadth,"-")
            screen.addstr(begin_y+height,breadth,"-")
        for length in range(begin_y,begin_y+height):
            screen.addstr(length,begin_x-1,"|")
            screen.addstr(length,begin_x+width,"|")
        if os.path.exists(filename): #check whether the file exists or not
            with open(filename) as data:
                cat = data.read()
            win.addstr(0,0,cat)
        screen.refresh() #updating screen with above data
        box = Textbox(win, True) #creating object of Textbox
        box.edit() #insert_mode = true
        msg = box.gather() #gathering input from user

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