"""You wake up with a splitting headache. The first thing you notice is that
it's pitch black, not a scrap of light to be found in... wherever you've ended
up. You feel around yourself, encountering nothing but sand covered stone. You
try to remember how you got here.

You had flown in to Cairo to meet your friend, Fulan Al Fulani, who had written
to you of a new and exciting find in the Pyramid of Djoser. Your bitter rival,
the Baron of Royston Vasey, had discovered the entrance to a secondary complex
of tunnels below the pyramid, and was quietly gathering supplies and workers to
excavate them. You had flown out the next day, intent on beating him to the
punch.

You see a light flare up in the darkness. "My Friend, are you all right?" With
a sigh of relief you see Fulan holding up a torch. With the added light, you can
see that you're standing in a narrow corridor, which branches off to the left
a few meters away. After seeing that you were uninjured, Fulan directs your
attention to a strange machine occupying the corridor with you.

It looks something like a large frog, but has an open hatch on the top. Climbing
in, the two of you spend a few hours puzzling over the inside, which includes a
lit screen with many lines drawn on it and an odd bank of controls. It appears
as if this machine is designed for navigating a maze, and after a few minutes of
exploring the corridors you find yourselves in, the diagram on the screen seems
to reflect them exactly.

With Fulan's help, you manage to translate the controls. There's a screen on
which you can punch in instructions for this frog-machine. Instructions can
include absolute directions: 'north', 'east', 'south' and 'west' and relative
directions: 'forward', 'right', 'backward' and 'left'. This machine will
probably prove invaluable in escaping your current predicament.

For this exercise, please edit the file maze/solution/exercise1.py
"""

from ..maze import Maze
from ..walker import Walker
from ..errors import BadCommand, Win
from ..displays.turtle_display import TurtleDisplay

def main():
    maze = Maze(5)
    maze._maze = [[13, 14, 8, 10, 9],
                  [6, 9, 5, 12, 1],
                  [13, 5, 7, 5, 5],
                  [5, 5, 12, 1, 5],
                  [6, 2, 3, 7, 7]]
    walker = Walker(maze)
    display = TurtleDisplay(maze)
    walker.power_on(display)

    from ..solution.exercise1 import instructions

    try:
        walker.run(instructions)
    except Win:
        msg = "Congratulations, you made it to the exit!"
    except BadCommand as err:
        msg = str(err)
    else:
        msg = "You didn't make it to the exit."
    print("{} Press q to quit.".format(msg))
    display.show()
