"""The maze itself.

Maze - A Maze to be walked through.
"""
from collections import deque
from random import sample, choice

class Maze:
    """A Randomized maze.

    Methods:
        dfs
        prim
        can_move

    Attributes:
        north_east - The coordinates of the top right cell of the maze.
    """

    # The maze is represented by a double list of 8-bit long ints. Each int
    # represents a cell of the maze and defines the walls around that cell, with
    # the lower 4 bits representing a wall and the upper 4 bits representing if
    # a wall is removable. The mapping is 0000 -> WSEN, with a 1 being a wall
    # for the lower 4 bits, and a 1 being a toggleable wall for the upper 4
    # bits. These three dicts are useful for operating on these ints. Bitwise
    # and with an entry in the _WALLCHECK dict will tell you if there is a wall
    # in a given direction. Bitwise and with an entry in the _WALLBREAK dict
    # will return a cell with the given wall removed and the other walls
    # unchanged. Bitwise and with an entry in the _TOGGLE dict will tell you if
    # the wall in that direction is toggleable.
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
    _TOGGLE = {
        'north': 16,
        'east': 32,
        'south': 64,
        'west': 128}

    def __init__(self, size):
        """Initialize the Maze and derive the north_east attribute.

        Positional Arguments:
            size - The number of maze cells per side.
        """
        self._size = size
        self.north_east = (size-1, size-1)
        self._maze = [[15 for i in range(size)] for j in range(size)]

    @property
    def size(self):
        """Read only property for size."""
        return self._size

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
            punched = False
            for neighbor in self._neighbors(coordinates):
                if neighbor in visited:
                    if not punched and neighbor != self.north_east:
                        self._punch_hole(neighbor, coordinates)
                        punched = True
                elif coordinates != self.north_east:
                    candidates.add(neighbor)
            candidates.remove(coordinates)
            visited.add(coordinates)

    _RELATIVE_COORDINATES = {
        'north': lambda x, y: (x, y+1),
        'east': lambda x, y: (x+1, y),
        'south': lambda x, y: (x, y-1),
        'west': lambda x, y: (x-1, y)}

    def _neighbors(self, coordinates):
        """Generate the coordinates of neighboring cells in random order.

        Positional Arguments:
            coordinates - The coordinates of the cell to get the neighbors of.

        Yields:
            neighbor - The coordinates of a random neighboring cell.
        """
        x, y = coordinates

        neighbors = {c: f(x, y) for c, f in self._RELATIVE_COORDINATES.items()}

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

    def toggle(self, coordinates, direction):
        """Check if we can toggle the given wall of a cell.

        Positional Arguments:
            coordinates: The coordinates of the cell we are moving from.
            direction: The direction to try and move.

        Returns:
            clear - A boolean representing if we can toggle the wall.

        Exceptions:
            IndexError - Raised if the coordinates are not inside the maze.
        """
        x, y = coordinates
        clear = False
        if self._maze[x][y] & self._TOGGLE[direction]:
            self._punch_hole(coordinates,
                             self._RELATIVE_COORDINATES[direction](x, y))
            clear = True
        return clear
