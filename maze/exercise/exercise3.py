"""*Crunch*

Well that certainly didn't sound good.

Another trapdoor had opened on you at the end of the last maze. You're really
getting tired of that at this point. At least you were somewhat prepared for it
this time. Taking stock, the machine still seems to be in working order, but
it's displaying another simple maze, and this time you can't seem to put in more
than three instructions.

After a little fiddling with the controls, Fulan finds a sheet of paper stuffed
behind one of the panels. It appears that the list of instructions can contain
lists of instructions, which can be repeated with numbers in the same way as
directions.

"Well, that solves that" says Fulan, "But this paper raises more questions than
it answers! It's written in a far more modern dialect than anything else we've
found in here. How strange." The two of you look at each other and Fulan shrugs.
"Well, perhaps we'll be able to figure it out once we're out of here."
"""

from .. import Maze, TooManyInstructions, Walker, Win

def main():
    maze = Maze(5)
    maze._maze = [[14, 9, 14, 10, 9],
                  [13, 6, 9, 13, 5],
                  [4, 10, 0, 1, 5],
                  [5, 14, 3, 6, 1],
                  [6, 10, 10, 11, 7]]
    walker = Walker(maze)
    walker.power_on()
    screen = walker._walker.getscreen()
    screen.onkey(screen.bye, 'q')
    screen.listen()

    from ..solution.exercise3 import instructions

    try:
        walker.run(instructions, 3)
    except Win:
        msg = "Congratulations, you made it to the exit!"
    except TooManyInstructions:
        msg = "The machine refuses to take that many instructions."
    else:
        msg = "You didn't make it to the exit."
    print("{} Press q to quit.".format(msg))
    screen.mainloop()
