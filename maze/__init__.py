"""Support classes for the maze walker exercise.

Maze - A Maze to be walked through.
Walker - A walker for the Maze.
"""
from collections import deque
from random import sample
from turtle import Turtle, TurtleScreen

class WalkerStateError(Exception):
    """An Error for trying to make the Walker do something it's not ready for."""
    pass

class BadCommandError(Exception):
    """An Error for a bad command in move's input."""
    pass

class Win(Exception):
    """An Exceptions to indicate that the win condition has been reached."""
    pass

class Maze:
    """A Randomized DFS maze.

    Methods:
        generate
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

    def generate(self):
        """Perform the randomized DFS to generate the maze.

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

class Walker:
    """A vehicle for traversing a treacherous maze.

    Methods:
        power_on
        move
        run
    """

    _RELATIVE_MAP = {
        'north': {'forward': 'north', 'right': 'east', 'backward': 'south', 'left': 'west'},
        'east': {'forward': 'east', 'right': 'south', 'backward': 'west', 'left': 'north'},
        'south': {'forward': 'south', 'right': 'west', 'backward': 'north', 'left': 'east'},
        'west': {'forward': 'west', 'right': 'north', 'backward': 'east', 'left': 'south'}}

    def __init__(self, maze):
        """Initialize the Walker.

        Positional Arguments:
            maze - The Maze that this Walker will be traversing.
        """
        self._maze = maze
        self._coordinates = (0, 0)
        self._walker = None
        self._direction_map = {
            'north': self._north,
            'east': self._east,
            'south': self._south,
            'west': self._west}
        self._relative_directions = self._RELATIVE_MAP['north']

    def power_on(self):
        """Turn on the Walker's lights, so you can see the Maze.

        Side Effects:
            Initializes self._walker.
        """
        self._walker = self._maze.draw()
        self._walker.speed(3)

    def move(self, direction, distance=1):
        """Attempt to move the walker a number of cells in the given direction.

        Positional Arguments:
            direction - The direction to attempt to move in. Can be either
                        absolute (north, south, east, west) or relative to
                        current heading (left, forward, right, backward).
            distance - How many cells to attempt to move. Moves in a straight
                       line whether direction is absolute or relative.

        Returns:
            success - If we were able to move the whole distance in the given direction.

        Exceptions:
            WalkerStateError - Raised if trying to move before the walker is powered.
            KeyError - Raised if the given direction is not valid.
            Win - Raised if the walker has reached the exit.

        Side Effects:
            May call functions which alter the Walker's coordinates and display.
        """
        if self._walker is None:
            raise WalkerStateError('Try calling power_on() first.')
        if direction in self._relative_directions:
            direction = self._relative_directions[direction]
        op = self._direction_map[direction]
        success = True
        for _ in range(distance):
            if not self._maze.can_move(self._coordinates, direction):
                success = False
                break
            op()
            self._relative_directions = self._RELATIVE_MAP[direction]
            if self._coordinates == self._maze.north_east:
                raise Win
        return success

    def _north(self):
        """Move the walker up one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._walker.setheading(90)
        self._walker.forward(10)
        self._coordinates = (self._coordinates[0], self._coordinates[1]+1)

    def _east(self):
        """Move the walker right one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._walker.setheading(0)
        self._walker.forward(10)
        self._coordinates = (self._coordinates[0]+1, self._coordinates[1])

    def _south(self):
        """Move the walker down one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._walker.setheading(270)
        self._walker.forward(10)
        self._coordinates = (self._coordinates[0], self._coordinates[1]-1)

    def _west(self):
        """Move the walker left one cell.

        Side Effects:
            Alters the Walker's coordinates and display.
        """
        self._walker.setheading(180)
        self._walker.forward(10)
        self._coordinates = (self._coordinates[0]-1, self._coordinates[1])

    def run(self, instructions):
        """Process a list of commands and attempt to move the Walker accordingly.

        Positional Arguments:
            instructions - A list of instructions for the Walker. Can be
                           directions or numbers, which will repeat the next
                           direction.

        Exceptions:
            BadCommandError - Raised for commands which are not directions.

        Side Effects:
            May call functions which alter the Walker's coordinates and display.
        """
        repeat = 1
        for i, instruction in enumerate(instructions):
            if isinstance(instruction, int):
                repeat = instruction
            elif isinstance(instruction, list):
                for _ in range(repeat):
                    self.run(instruction)
                repeat = 1
            else:
                try:
                    self.move(instruction, repeat)
                except (KeyError, TypeError):
                    raise BadCommandError('position {}.'.format(i))
                repeat = 1
