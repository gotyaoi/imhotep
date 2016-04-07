"""The framework for the exercises."""
from collections import defaultdict
from importlib import import_module
from pathlib import Path

from .. import Maze, Walker, TurtleDisplay
from ..errors import BadCommand, TooManyInstructions, Win

def exercise(user_func, size=5, algo='dfs', fields=None):
    """Handle common exercise setup."""
    if fields:
        maze = Maze(len(fields))
        maze._maze = fields
    else:
        maze = maze(size)
        getattr(maze, algo)()
    walker = Walker(maze)
    display = TurtleDisplay(maze)
    walker.power_on(display)

    try:
        user_func(walker)
    except Win:
        msg = "Congratulations, you made it to the exit!"
    except TooManyInstructions:
        msg = "The machine refuses to take that many instructions."
    except BadCommand as err:
        msg = str(err)
    else:
        msg = "You didn't make it to the exit."
    print("{} Press q to quit.".format(msg))
    display.show()

def discover():
    """Find and get the registry details of all exercises."""
    registry = defaultdict(dict)
    base = Path(__file__).parent
    for path in base.glob('*.py'):
        if path.name == '__init__.py' or path.name == 'framework.py':
            continue
        exercise_module = import_module('maze.exercise.'+path.stem)
        solution_module = import_module('maze.solution.'+path.stem)
        details = exercise_module.register()
        registry[details['category']][details['name']] = [exercise_module, solution_module]
    return registry
