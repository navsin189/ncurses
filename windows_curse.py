import curses

# all the print statement will be printed on standard output
print("initializing new screen")

screen = curses.initscr()
print("Screen initialized.")
my_window = curses.newwin(15, 20, 0, 0)
my_window.addstr(4, 4, "Hello from 4,4")
my_window.addstr(5, 15, "Hello from 5,15 with a long string")

# Print the window to the screen
my_window.refresh()
curses.napms(2000)
#adding string/text on the new screen

screen.refresh() #screen should be refreshed to display the text. It  update the screen

curses.napms(2000) #it holds the screen for particular time
curses.endwin() #close/exit the screen

print("Window ended.")