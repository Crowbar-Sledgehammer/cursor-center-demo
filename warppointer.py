#!/usr/bin/env python
"""Make the X cursor wrap-around.

Adapted from http://appdb.winehq.org/objectManager.php?sClass=version&iId=12599
to work around lack of relative mouse movement http://wiki.winehq.org/Bug6971
for Thief: Dark Shadows (and possibly others)

This version is a little kinder to your CPU than the shell script with
the busy-loop that starts a new process for every pointer query.
"""
from ctypes import cdll, c_int, c_voidp, byref
import time

xlib = cdll.LoadLibrary('libX11.so.6')

# Maximum screen width and height
MAX_X = 1280
MAX_Y = 1024

# Number of seconds to sleep between polling mouse position.
SLEEPTIME = 0.05

class Cursor(object):
    """docstring for Cursor"""
    def __init__(self, display, window_title=None):
        super(Cursor, self).__init__()
        self.display = display
        self.window_title = window_title

        self.root = xlib.XDefaultRootWindow(self.display)
        self.mousex = c_int()
        self.mousey = c_int()
        # pointer for unused return values
        self.unused_int = c_int()
        # likewise, querypointer wants a window pointer to write to.  We don't
        # really want to create a new window, but this was the shortest way I
        # could think of to get the memory allocated.
        self.tmp_win = c_voidp(xlib.XCreateSimpleWindow(
            self.display, self.root, 0, 0, 1, 1, 0, 0, 0
        ))

    def reset_mouse(self, xpos, ypos):
        """
            reset_mouse
        """
        xlib.XWarpPointer(self.display, None, self.root, 0, 0, 0, 0, xpos, ypos)

    def get_mouse(self):
        """
            get_mouse
        """
        xlib.XQueryPointer(
            self.display, self.root,
            byref(self.tmp_win), byref(self.tmp_win),
            byref(self.mousex), byref(self.mousey),
            byref(self.unused_int),
            byref(self.unused_int),
            byref(self.unused_int)
        )

    def main(self):
        """
            main
        """
        while True:
            self.get_mouse()
            if self.mousex.value < 2:
                self.reset_mouse(xpos=MAX_X-2, ypos=self.mousey.value)
            elif self.mousex.value > (MAX_X-2):
                self.reset_mouse(xpos=2, ypos=self.mousey.value)
            time.sleep(SLEEPTIME)

class Display(object):
    """docstring for Display"""

    _display = None

    def __init__(self, display=None):
        super(Display, self).__init__()
        self.display = display

    def __enter__(self):
        self._display = xlib.XOpenDisplay(self.display)
        return self._display

    def __exit__(self, _type, value, traceback):
        xlib.XCloseDisplay(self._display)

def main():
    """
        main
    """
    with Display() as display:
        Cursor(display).main()


if __name__ == '__main__':
    main()
