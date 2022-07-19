# ncurses

## History

ncurses (new curses) is a programming library providing an application programming interface (API) that allows the programmer to write text-based user interfaces in a terminal-independent manner. It is a toolkit for developing "GUI-like" application software that runs under a terminal emulator. It also optimizes screen changes, in order to reduce the latency experienced when using remote shells.

[Click here for brief history](https://tldp.org/HOWTO/NCURSES-Programming-HOWTO/intro.html)

> Nano text editor is a good example of ncurse

## Practical Implementation

- operating system: Ubuntu
- language: Python 3.10

```
#!/usr/bin/python3
import curses

# all the print statement will be printed on standard outpu
print("initializing new screen")
screen = curses.initscr()
print("Screen initialized.")
screen.refresh() #screen should be refreshed to display the text. It update the screen
curses.napms(2000) #it holds the screen for particular time
curses.endwin() #close/exit the screen
print("Window ended.")
```

- importing curses(comes by default with Linux)
- for windows `python -m pip install windows-curses`
- initializing new screen using `initscr()`. A black screen will be rendered.
- `screen.refresh()` is used to display the text/information because the text is not rendered instantly. This is because curses was originally written with slow 300-baud terminal connections in mind; with these terminals, minimizing the time required to redraw the screen was very important. **without this the black screen will not be shown to user.**
- napms() will render the screen only for the specified time.
- endwin() terminate the screen.
- **all the print statement will be printed on base terminal not on screen.**
