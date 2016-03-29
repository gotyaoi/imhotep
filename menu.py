"""The interactive menu for the maze exercises."""
import sys
if sys.version_info.major != 3 or sys.version_info.minor < 4:
    sys.exit('Python 3.4 or greater is required.')

from cmd import Cmd
from importlib import import_module, reload
from pathlib import Path

import readline
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")

class MyCmd(Cmd):
    """Base class with some specialized exit commands."""

    QUIT = {'q', 'exit', 'bye', 'EOF'}

    def emptyline(self):
        pass

    def default(self, line):
        cmd, _, line = self.parseline(line)
        if cmd in self.QUIT:
            if cmd == 'EOF':
                self.stdout.write('\n')
            return True
        return super().default(line)

    def do_quit(self, _):
        """Go up one menu, or quit if this is the top menu."""
        return True

class Outer(MyCmd):
    """Menu listing all the exercises."""

    EXERCISES = {x.stem for x in Path('maze/exercise').glob('exercise*')}

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
Please choose an exercise. Available exercises:\n''' + '\n'.join(sorted(EXERCISES))
    prompt = '> '

for _exercise in Outer.EXERCISES:
    setattr(Outer, 'do_'+_exercise, lambda self, arg, ex=_exercise: Inner(ex).cmdloop())
    setattr(getattr(Outer, 'do_'+_exercise), '__doc__', 'submenu for {}.'.format(_exercise))

class Inner(MyCmd):
    """Menu customizable for each exercise."""

    def __init__(self, exercise, *args, **kwargs):
        self.exercise = exercise
        self.exercise_module = import_module('maze.exercise.' + exercise)
        self.solution_module = None
        self.intro = '''Available Commands:
story - {}
run - {}
quit - {}'''.format(self.do_story.__doc__, self.do_run.__doc__, self.do_quit.__doc__)
        self.prompt = exercise + '> '
        super().__init__(*args, **kwargs)

    def do_story(self, _):
        """Print the story and other useful information for this exercise."""
        print(self.exercise_module.__doc__)

    def do_run(self, _):
        """Run the exercise."""
        try:
            if self.solution_module is None:
                self.solution_module = import_module('maze.solution.' + self.exercise)
            else:
                self.solution_module = reload(self.solution_module)
        except SyntaxError as err:
            print('''You seem to have a syntax error in your solution file:
{}, Line: {}, Character: {}'''.format(err.args[0], err.args[1][1], err.args[1][2]))
        else:
            self.exercise_module.main()

if __name__ == '__main__':
    Outer().cmdloop()
