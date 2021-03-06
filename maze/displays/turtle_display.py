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
        self._imhotep = None

    def draw(self):
        """Create a turtle and draw the maze.

        Returns:
            imhotep - The maze turtle, positioned in the bottom left cell.
        """
        turtle.TurtleScreen._RUNNING = True # workaround for python3.5
        imhotep = turtle.Turtle()
        self._imhotep = imhotep
        imhotep.screen.setworldcoordinates(0, 0, self._maze.size*10, self._maze.size*10)
        imhotep.hideturtle()
        imhotep.penup()
        imhotep.speed(0)
        oldtracer = imhotep.screen.tracer()
        imhotep.screen.tracer(1000)
        for x in range(self._maze.size):
            for y in range(self._maze.size):
                cell = (x, y)
                for direction in ['north', 'east', 'south', 'west']:
                    if not self._maze.can_move(cell, direction):
                        self._draw_wall(cell, direction)
                if cell == self._maze.north_east:
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

    _DRAW_START = {
        'north': lambda x, y: ((x*10, (y+1)*10), 0),
        'east': lambda x, y: (((x+1)*10, y*10), 90),
        'south': lambda x, y: ((x*10, y*10), 0),
        'west': lambda x, y: ((x*10, y*10), 90)}

    def _draw_wall(self, coordinates, direction):
        start, heading = self._DRAW_START[direction](*coordinates)
        self._imhotep.setposition(*start)
        self._imhotep.setheading(heading)
        self._imhotep.pendown()
        self._imhotep.forward(10)
        self._imhotep.penup()

    def north(self):
        """Move the walker up one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._imhotep.setheading(90)
        self._imhotep.forward(10)

    def east(self):
        """Move the walker right one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._imhotep.setheading(0)
        self._imhotep.forward(10)

    def south(self):
        """Move the walker down one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._imhotep.setheading(270)
        self._imhotep.forward(10)

    def west(self):
        """Move the walker left one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._imhotep.setheading(180)
        self._imhotep.forward(10)

    def show(self):
        """Block until user presses q."""
        self._imhotep.getscreen().mainloop()

    def toggle(self, coordinates, direction):
        old_position = self._imhotep.position()
        old_heading = self._imhotep.heading()
        self._imhotep.speed(0)
        stamp = self._imhotep.stamp()
        self._imhotep.hideturtle()
        self._imhotep.color('white')
        self._draw_wall(coordinates, direction)
        self._imhotep.setposition(old_position)
        self._imhotep.setheading(old_heading)
        self._imhotep.speed(3)
        self._imhotep.showturtle()
        self._imhotep.color('black')
        self._imhotep.clearstamp(stamp)
