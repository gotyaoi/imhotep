"""The interactive menu for the maze exercises."""
from cmd import Cmd
from importlib import import_module, reload
from pathlib import Path


class MyCmd(Cmd):
    """Base class with some specialized exit commands."""

    QUIT = {'q', 'quit', 'exit', 'bye', 'EOF'}

    def emptyline(self):
        pass

for _quit in MyCmd.QUIT:
    if _quit == 'EOF':
        setattr(MyCmd, 'do_'+_quit, lambda self, arg: print() or True)
    else:
        setattr(MyCmd, 'do_'+_quit, lambda self, arg: True)
    setattr(getattr(MyCmd, 'do_'+_quit), '__doc__',
            'Go up one level, or quit if this is the top level.')

class Outer(MyCmd):
    """Menu listing all the exercises."""

    EXERCISES = {x.stem for x in Path('maze/exercise').glob('*.py')}

    intro = 'Please choose an exercise. Available exercises:\n' + '\n'.join(EXERCISES)
    prompt = '> '

for _exercise in Outer.EXERCISES:
    setattr(Outer, 'do_'+_exercise, lambda self, arg, ex=_exercise: Inner(ex).cmdloop())
    setattr(getattr(Outer, 'do_'+_exercise), '__doc__', 'submenu for {}.'.format(_exercise))

class Inner(MyCmd):
    """Menu customizable for each exercise."""

    def __init__(self, exercise, *args, **kwargs):
        self.exercise = exercise
        self.exercise_module = import_module('maze.exercise.' + exercise)
        self.solution_module = import_module('maze.solution.' + exercise)
        self.intro = exercise + ':\ninfo\nreload\nrun\nquit'
        self.prompt = exercise + '> '
        super().__init__(*args, **kwargs)

    def do_info(self, _):
        """Print the story and other useful information for this exercise."""
        print(self.exercise_module.__doc__)

    def do_reload(self, _):
        """Reload the solution module. Run this after editing the module."""
        self.solution_module = reload(self.solution_module)

    def do_run(self, _):
        """Run the exercise."""
        self.exercise_module.main()

if __name__ == '__main__':
    Outer().cmdloop()
