"""The walker for navigating the maze.

Walker - A walker for the Maze.
"""

from .errors import WalkerStateError, BadCommand, TooManyInstructions, Win

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

    def run(self, instructions, limit=0):
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
        count = 0
        repeat = 1
        for i, instruction in enumerate(instructions):
            if limit > 0 and count >= limit:
                raise TooManyInstructions
            if isinstance(instruction, int):
                count += 1
                repeat = instruction
            elif isinstance(instruction, list):
                for _ in range(repeat):
                    self.run(instruction, limit)
                count += len(instruction)
                repeat = 1
            else:
                try:
                    self.move(instruction, repeat)
                except (KeyError, TypeError):
                    raise BadCommand('Bad command at position {}.'.format(i))
                count += 1
                repeat = 1
        return count
