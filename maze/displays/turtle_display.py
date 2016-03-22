"""Turtle backend for the maze display.

TurtleDisplay - A Turtle based display for the maze.
"""
import turtle

class TurtleDisplay:
    """A display for showing the maze to the user, using Turtle.

    Methods:
        draw
    """
    def __init__(self, maze):
        self._maze = maze
        self._turtle = None

    def draw(self):
        """Create a turtle and draw the maze.

        Returns:
            imhotep - The maze turtle, positioned in the bottom left cell.
        """
        turtle.TurtleScreen._RUNNING = True # workaround for python3.5
        imhotep = turtle.Turtle()
        imhotep.screen.setworldcoordinates(0, 0, self._maze._size*10, self._maze._size*10)
        imhotep.hideturtle()
        imhotep.penup()
        imhotep.speed(0)
        oldtracer = imhotep.screen.tracer()
        imhotep.screen.tracer(1000)
        for x in range(self._maze._size):
            for y in range(self._maze._size):
                cell = self._maze._maze[x][y]
                if cell & self._maze._WALLCHECK['north']:
                    imhotep.setposition(x*10, (y+1)*10)
                    imhotep.setheading(0)
                    imhotep.pendown()
                    imhotep.forward(10)
                    imhotep.penup()
                if cell & self._maze._WALLCHECK['east']:
                    imhotep.setposition((x+1)*10, y*10)
                    imhotep.setheading(90)
                    imhotep.pendown()
                    imhotep.forward(10)
                    imhotep.penup()
                if cell & self._maze._WALLCHECK['south']:
                    imhotep.setposition(x*10, y*10)
                    imhotep.setheading(0)
                    imhotep.pendown()
                    imhotep.forward(10)
                    imhotep.penup()
                if cell & self._maze._WALLCHECK['west']:
                    imhotep.setposition(x*10, y*10)
                    imhotep.setheading(90)
                    imhotep.pendown()
                    imhotep.forward(10)
                    imhotep.penup()
                if (x, y) == self._maze.north_east:
                    #draw smaller square
                    imhotep.setposition(x*10+2, y*10+2)
                    imhotep.setheading(90)
                    imhotep.pendown()
                    for _ in range(4):
                        imhotep.forward(6)
                        imhotep.right(90)
                    #draw an x
                    imhotep.setheading(45)
                    imhotep.pendown()
                    imhotep.setposition(x*10+8, y*10+8)
                    imhotep.penup()
                    imhotep.setposition(x*10+2, y*10+8)
                    imhotep.setheading(-45)
                    imhotep.pendown()
                    imhotep.setposition(x*10+8, y*10+2)
                    imhotep.penup()
        imhotep.screen.tracer(oldtracer)
        imhotep.setposition(5, 5)
        imhotep.setheading(90)
        imhotep.speed(3)
        imhotep.showturtle()
        screen = imhotep.getscreen()
        screen.onkey(screen.bye, 'q')
        screen.listen()
        self._turtle = imhotep

    def north(self):
        """Move the walker up one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._turtle.setheading(90)
        self._turtle.forward(10)

    def east(self):
        """Move the walker right one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._turtle.setheading(0)
        self._turtle.forward(10)

    def south(self):
        """Move the walker down one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._turtle.setheading(270)
        self._turtle.forward(10)

    def west(self):
        """Move the walker left one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._turtle.setheading(180)
        self._turtle.forward(10)

    def show(self):
        self._turtle.getscreen().mainloop()
