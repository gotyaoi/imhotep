from cmd import Cmd
from importlib import import_module, reload
from pathlib import Path


class MyCmd(Cmd):

    QUIT = set(('q', 'quit', 'exit', 'bye', 'EOF'))

    def emptyline(self):
        pass

    def default(self, line):
        cmd, _, line = self.parseline(line)
        if cmd == 'EOF':
            print()
        if cmd in self.QUIT:
            return True
        super().default(line)

class Outer(MyCmd):

    EXERCISES = [x.stem for x in Path('maze/exercise').glob('*.py')]

    intro = 'Please choose an exercise. Available exercises:\n' + '\n'.join(EXERCISES)
    prompt = '> '

    def onecmd(self, line):
        cmd, _, line = self.parseline(line)
        if cmd not in self.EXERCISES:
            return super().onecmd(line)
        inner = Inner(cmd)
        inner.cmdloop()

class Inner(MyCmd):

    def __init__(self, exercise, *args, **kwargs):
        self.exercise = exercise
        self.exercise_module = import_module('maze.exercise.' + exercise)
        self.solution_module = import_module('maze.solution.' + exercise)
        self.intro = exercise + ':\ninfo\nreload\nrun\nquit'
        self.prompt = exercise + '> '
        super().__init__(*args, **kwargs)

    def do_info(self, arg):
        print(self.exercise_module.__doc__)

    def do_reload(self, arg):
        self.solution_module = reload(self.solution_module)

    def do_run(self, arg):
        self.exercise_module.main()

if __name__ == '__main__':
    interp = Outer()
    interp.cmdloop()
