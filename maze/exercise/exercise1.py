from sys import exit

from .. import Maze, Walker, Win

m = Maze(5)
m._maze = [[13, 14, 8, 10, 9],
           [6, 9, 5, 12, 1],
           [13, 5, 7, 5, 5],
           [5, 5, 12, 1, 5],
           [6, 2, 3, 7, 7]]
w = Walker(m)
w.power_on()
w._walker.screen.onkey(exit, 'q')
w._walker.screen.listen()

from ..solution.solution1 import instructions

try:
    w.run(instructions)
except Win:
    print("Congratulations, you made it to the exit! Press q to quit.")
else:
    print("You didn't make it to the exit. Press q to quit")
w._walker.screen.mainloop()
