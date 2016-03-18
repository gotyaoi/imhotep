"""As the machine rumbles to the exit, you feel the floor drop out from under
you. A trapdoor has opened underneath you, dropping you, Fulan and the machine
farther from the exit than where you began. With a loud thump, the machine
lands on the lower floor. After a short time spent contemplating how comfortable
the floor is, you pick yourself up, check on Fulan, and have a look around.

Despite how far you seemed to fall, the machine is in fairly good shape. Good
thing too, as it appears that you've landed at the entrance of another maze.
Heading back into the cabin, you see Fulan puzzling over the display. "The
layout of this maze is fairly straightforward" he says, "simply travelling east
and then north, but I can't seem to input more than four instructions this
time! How on earth are we going to get out of here now?"

After examining the controls further, the two of you make a discovery. It
appears that in addition to directions, numbers can also be given to the
machine. A number will cause the following instruction to be repeated the
specified number of times. Fulan smiles, "Well, that's fairly simple. Care to do
the honors my friend?"
"""

from .. import Maze, Walker, Win

def main():
    maze = Maze(5)
    maze._maze = [[13, 12, 8, 10, 9],
                  [4, 3, 5, 13, 5],
                  [5, 12, 3, 5, 5],
                  [5, 7, 13, 6, 3],
                  [6, 10, 2, 10, 11]]
    walker = Walker(maze)
    walker.power_on()
    screen = walker._walker.getscreen()
    screen.onkey(screen.bye, 'q')
    screen.listen()

    from ..solution.exercise2 import instructions

    try:
        walker.run(instructions)
    except Win:
        print("Congratulations, you made it to the exit! Press q to quit.")
    else:
        print("You didn't make it to the exit. Press q to quit")
    screen.mainloop()
