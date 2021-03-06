"""Well, at least it was a short fall this time, you think, right before a chunk
of metal falls directly on your head. Ow. Rubbing your now bruised skull, you
pick up the piece of metal and chuck it to the back of the machine in annoyance.
A second later, a glimmer of recognition sparks in your mind...

"The paper tape reader!" exclaims fulan, pointing at the gaping hole in the
instrument panel where you had been feeding in the instruction lists. You
glance over at the chunk of metal now lying on the floor in several pieces.

Oops.

After a few minutes of berating your own stupidity and trying to piece the
reader back together, Fulan calls you over. He had been studying the mass of
gears and belts and other assorted machinery that the absence of the reader had
revealed. "I think I've located where the reader was attached to." he says,
pointing to a group of buttons close to the edge of the hole. "These buttons are
in a similar pattern to the instructions we've been feeding the machine. It
might be possible to manipulate them directly and still manage to control the
machine." He looks at you grimly. "I don't think you'll lose your hand, but we
can't be sure. You get to work and I'll get some gauze ready.
"""
from .framework import exercise

def user_func(walker):
    from ..solution.exercise4 import hand
    hand(walker.run)

def main():
    maze = [[12, 10, 10, 8, 11],
            [6, 11, 12, 0, 9],
            [14, 10, 1, 7, 5],
            [12, 8, 0, 9, 7],
            [7, 7, 7, 6, 11]]
    exercise(user_func, fields=maze)

def register():
    return {'name': '1_calling_functions', 'category': '2_Control_Structures'}
