"""The maze itself.

Maze - A Maze to be walked through.
"""
from collections import deque
from random import sample, choice
from turtle import Turtle, TurtleScreen

class Maze:
    """A Randomized maze.

    Methods:
        dfs
        prim
        draw
        can_move

    Attributes:
        north_east - The coordinates of the top right cell of the maze.
    """

    # The maze is represented by a double list of 4-bit long ints. Each int
    # represents a cell of the maze and defines the walls around that cell, with
    # each bit representing a wall. The mapping is 0000 -> WSEN, with a 1 being
    # a wall and a 0 being no wall. These two dicts are useful for operating on
    # these ints. Bitwise and with an entry in the _WALLCHECK dict will tell
    # you if there is a wall in a given direction. Bitwise and with an entry in
    # the _WALLBREAK dict will return a cell with the given wall removed and the
    # other walls unchanged.
    _WALLCHECK = {
        'north': 1,
        'east': 2,
        'south': 4,
        'west': 8}
    _WALLBREAK = {
        'north': 14,
        'east': 13,
        'south': 11,
        'west': 7}

    def __init__(self, size):
        """Initialize the Maze and derive the north_east attribute.

        Positional Arguments:
            size - The number of maze cells per side.
        """
        self._size = size
        self.north_east = (size-1, size-1)
        self._maze = [[15 for i in range(size)] for j in range(size)]

    def dfs(self):
        """Perform randomized DFS to generate the maze.

        Uses a stack of generators to perform the backtracking instead of
        recursion. I like big mazes and I cannot lie.

        Side Effects:
            Modifies self._maze in place.
        """
        coordinates = (0, 0)
        visited = set()
        stack = deque()
        while True:
            visited.add(coordinates)
            try:
                if coordinates == self.north_east:
                    raise StopIteration
                gen = self._neighbors(coordinates)
                while True:
                    neighbor = next(gen)
                    if neighbor not in visited:
                        break
                self._punch_hole(coordinates, neighbor)
                stack.append((coordinates, gen))
                coordinates = neighbor
            except StopIteration:
                if coordinates == (0, 0):
                    break
                coordinates, gen = stack.pop()

    def prim(self):
        """Perform randomized Prim's Algorithm to generate the maze.

        Side Effects:
            Modifies self._maze in place.
        """
        visited = {(0, 0)}
        candidates = {(0, 1), (1, 0)}
        while candidates:
            coordinates = choice(sorted(candidates))
            neighbors = list(self._neighbors(coordinates))
            punched = False
            for neighbor in neighbors:
                if neighbor in visited:
                    if not punched:
                        self._punch_hole(neighbor, coordinates)
                        punched = True
                else:
                    candidates.add(neighbor)
            candidates.remove(coordinates)
            visited.add(coordinates)

    def _neighbors(self, coordinates):
        """Generate the coordinates of neighboring cells in random order.

        Positional Arguments:
            coordinates - The coordinates of the cell to get the neighbors of.

        Yields:
            neighbor - The coordinates of a random neighboring cell.
        """
        x, y = coordinates
        neighbors = {'east': (x+1, y),
                     'west': (x-1, y),
                     'north': (x, y+1),
                     'south': (x, y-1)}
        if x == 0:
            del neighbors['west']
        elif x == self._size-1:
            del neighbors['east']
        if y == 0:
            del neighbors['south']
        elif y == self._size-1:
            del neighbors['north']
        for neighbor in sample(list(neighbors.values()), len(neighbors)):
            yield neighbor

    def _punch_hole(self, start_coordinates, end_coordinates):
        """Removes the walls between two adjacent cells.

        Positional Arguments:
            start_coordinates - The coordinates of the first cell.
            end_coordinates - The coordinates of the second cell.

        Exceptions:
            ValueError - Raised if the given coordinates are not adjacent.
            IndexError - Raised if the coordinates are not inside the maze.

        Side Effects:
            Modifies self._maze in place.
        """
        start_x, start_y = start_coordinates
        end_x, end_y = end_coordinates
        if start_x == end_x:
            if end_y - start_y == 1:
                self._maze[start_x][start_y] &= self._WALLBREAK['north']
                self._maze[end_x][end_y] &= self._WALLBREAK['south']
            elif end_y - start_y == -1:
                self._maze[start_x][start_y] &= self._WALLBREAK['south']
                self._maze[end_x][end_y] &= self._WALLBREAK['north']
            else:
                raise ValueError('Coordinates are not adjacent')
        elif start_y == end_y:
            if end_x - start_x == 1:
                self._maze[start_x][start_y] &= self._WALLBREAK['east']
                self._maze[end_x][end_y] &= self._WALLBREAK['west']
            elif end_x - start_x == -1:
                self._maze[start_x][start_y] &= self._WALLBREAK['west']
                self._maze[end_x][end_y] &= self._WALLBREAK['east']
            else:
                raise ValueError('Coordinates are not adjacent')
        else:
            raise ValueError('Coordinates are not adjacent')

    def draw(self):
        """Create a turtle and draw the maze.

        Returns:
            imhotep - The maze turtle, positioned in the bottom left cell.
        """
        TurtleScreen._RUNNING = True # workaround for python3.5
        imhotep = Turtle()
        imhotep.screen.setworldcoordinates(0, 0, self._size*10, self._size*10)
        imhotep.hideturtle()
        imhotep.penup()
        imhotep.speed(0)
        oldtracer = imhotep.screen.tracer()
        imhotep.screen.tracer(1000)
        for x in range(self._size):
            for y in range(self._size):
                cell = self._maze[x][y]
                if cell & self._WALLCHECK['north']:
                    imhotep.setposition(x*10, (y+1)*10)
                    imhotep.setheading(0)
                    imhotep.pendown()
                    imhotep.forward(10)
                    imhotep.penup()
                if cell & self._WALLCHECK['east']:
                    imhotep.setposition((x+1)*10, y*10)
                    imhotep.setheading(90)
                    imhotep.pendown()
                    imhotep.forward(10)
                    imhotep.penup()
                if cell & self._WALLCHECK['south']:
                    imhotep.setposition(x*10, y*10)
                    imhotep.setheading(0)
                    imhotep.pendown()
                    imhotep.forward(10)
                    imhotep.penup()
                if cell & self._WALLCHECK['west']:
                    imhotep.setposition(x*10, y*10)
                    imhotep.setheading(90)
                    imhotep.pendown()
                    imhotep.forward(10)
                    imhotep.penup()
                if (x, y) == self.north_east:
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
        imhotep.speed(6)
        imhotep.setposition(5, 5)
        imhotep.setheading(90)
        imhotep.showturtle()
        return imhotep

    def can_move(self, coordinates, direction):
        """Check if we can move from the given coordinates in the given direction.

        Positional Arguments:
            coordinates: The coordinates of the cell we are moving from.
            direction: The direction to try and move.

        Returns:
            clear - A boolean representing if we can move.

        Exceptions:
            IndexError - Raised if the coordinates are not inside the maze.
        """
        x, y = coordinates
        clear = True
        if self._maze[x][y] & self._WALLCHECK[direction]:
            clear = False
        return clear
