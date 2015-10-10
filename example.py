#!/usr/bin/env python

import window
import os

import cursor

class ExampleWindow(window.Window):
    """
        Gui application interface.
    """

    GLADE_FILE = os.path.splitext(__file__)[0] + '.glade'

    def __init__(self):
        super(ExampleWindow, self).__init__()


    class Handler(window.Window.BaseHandler):
        sizex = 300
        sizey = 200
        """
            Main Window Event Handler
        """
        def on_drawingarea1_draw(self, widget, cairo_ct):
            """
                Draw Diagnostic Marks
            """
            self.sizex = widget.get_allocated_width()
            self.sizey = widget.get_allocated_height()
            cairo_ct.set_source_rgb(0, 0, 0)
            cairo_ct.move_to(0 * self.sizex, 0 * self.sizey)
            cairo_ct.line_to(1 * self.sizex, 1 * self.sizey)
            cairo_ct.move_to(1 * self.sizex, 0 * self.sizey)
            cairo_ct.line_to(0 * self.sizex, 1 * self.sizey)
            cairo_ct.set_line_width(20)
            cairo_ct.stroke()

            cairo_ct.rectangle(0*self.sizex, 0*self.sizey, 0.5*self.sizex, 0.5*self.sizey)
            cairo_ct.set_source_rgba(1, 0, 0, 0.80)
            cairo_ct.fill()

            cairo_ct.rectangle(0*self.sizex, 0.5*self.sizey, 0.5*self.sizex, 0.5*self.sizey)
            cairo_ct.set_source_rgba(0, 1, 0, 0.60)
            cairo_ct.fill()

            cairo_ct.rectangle(0.5*self.sizex, 0*self.sizey, 0.5*self.sizex, 0.5*self.sizey)
            cairo_ct.set_source_rgba(0, 0, 1, 0.40)
            cairo_ct.fill()


        def on_button1_clicked(self, widget):
            _, winx, winy = widget.get_window().get_origin()

            offx, offy = widget.translate_coordinates(widget.get_toplevel(), 0, -self.sizey)

            xpos = winx + offx + (self.sizex // 2)
            ypos = winy + offy + (self.sizey // 2)

            with cursor.Display() as display:
                cursor.Cursor(display).reset_mouse(xpos, ypos)



if __name__ == '__main__':
    exit(ExampleWindow().main())
