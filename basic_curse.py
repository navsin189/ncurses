import curses

# all the print statement will be printed on standard output
print("initializing new screen")

screen = curses.initscr()
print("Screen initialized.")

#adding string/text on the new screen

screen.refresh() #screen should be refreshed to display the text. It  update the screen

curses.napms(2000) #it holds the screen for particular time
curses.endwin() #close/exit the screen

print("Window ended.")