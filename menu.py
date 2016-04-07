"""The interactive menu for the maze exercises."""
import readline
import sys

from cmd import Cmd
from importlib import reload

from maze.exercise.framework import discover

if sys.version_info.major != 3 or sys.version_info.minor < 4:
    sys.exit('Python 3.4 or greater is required.')

_REGISTRY = discover()

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")

class MyCmd(Cmd):
    """Base class with some specialized exit commands."""

    _QUIT = {'q', 'exit', 'bye', 'EOF'}

    def emptyline(self):
        pass

    def default(self, line):
        cmd, _, line = self.parseline(line)
        if cmd in self._QUIT:
            if cmd == 'EOF':
                self.stdout.write('\n')
            return True
        return super().default(line)

    def do_quit(self, _):
        """Go up one menu, or quit if this is the top menu."""
        return True

    def get_names(self):
        return dir(self)

class Outer(MyCmd):
    """Menu listing all the exercises."""

    intro = '''
     _.mmmmmmmmm._
   dMMMY'~~~~~`YMMMb
 dMMMY'         `YMMMb
dMMMY'           `YMMMb
CMMM(             )MMMD
YMMMb.           .dMMMY
 YMMMb.         .dMMMY
  `YMMMboo...oodMMMY'
.    `"#MMMMMMM#"'    .
Mb       `MMM'       dM
MMMM.   .dMMMb.   .dMMM
MMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMM
MMMM'   `YMMMY'   `YMMM
MM'      )MMM(      `MM
'       .MMMMM.       `
        dMMMMMb
       dMMMMMMMb
        """""""
Welcome to the Imhotep menu. Type in commands followed by the enter key.
Use the command "help" to get a list of available commands, and "help <command>"
to get help about a specific command. Use the command "quit" to exit the menu.
Please choose a category. Available Categories:\n''' + '\n'.join(sorted(_REGISTRY))
    prompt = '\n> '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for category in _REGISTRY:
            # Manually bind the function to the instance.
            setattr(self, 'do_'+category,
                    self._generator(category).__get__(self, Outer))

    @staticmethod
    def _generator(category_name):
        """Create a do_ function for a given category"""
        def do_category(self, _):
            Category(category_name).cmdloop()
        do_category.__name__ = 'do_' + category_name
        do_category.__doc__ = """Submenu for {}.""".format(category_name)
        return do_category

class Category(MyCmd):
    """Menu customizable for each category."""
    def __init__(self, category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intro = 'Available Exercises:\n' + '\n'.join(sorted(_REGISTRY[category]))
        self.prompt = '\n' + category + '> '
        for exercise in _REGISTRY[category]:
            # Manually bind the function to the instance.
            setattr(self, 'do_'+exercise,
                    self._generator(category, exercise).__get__(self, Category))

    @staticmethod
    def _generator(category_name, exercise_name):
        """Create a do_ function for a given exercise"""
        def do_exercise(self, _):
            Exercise(category_name, exercise_name).cmdloop()
        do_exercise.__name__ = 'do_' + exercise_name
        do_exercise.__doc__ = """Submenu for {}.""".format(exercise_name)
        return do_exercise

class Exercise(MyCmd):
    """Menu customizable for each exercise."""

    def __init__(self, category, exercise, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modules = _REGISTRY[category][exercise]
        self.intro = '''Available Commands:
story - {}
run - {}
quit - {}'''.format(self.do_story.__doc__, self.do_run.__doc__, self.do_quit.__doc__)
        self.prompt = '\n' + category + '/' + exercise + '> '

    def do_story(self, _):
        """Print the story and other useful information for this exercise."""
        print(self.modules[0].__doc__)

    def do_run(self, _):
        """Run the exercise."""
        try:
            self.modules[1] = reload(self.modules[1])
        except SyntaxError as err:
            print('''You seem to have a syntax error in your solution file:
{}, Line: {}, Character: {}'''.format(err.args[0], err.args[1][1], err.args[1][2]))
        else:
            self.modules[0].main()

if __name__ == '__main__':
    Outer().cmdloop()
