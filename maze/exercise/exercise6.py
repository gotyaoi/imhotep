"""As you stare at the screen on the walker, you wonder how you're going to get
out of this one. You seem completely blocked in. You probably need to open
one of the walls in the way, but which one? As you drive past one of them, the
panel under Fulan's hand pulses softly.

"Ah, Open Sesame!" Fulan quickly says the magic words and the wall slides up.
"How interesting, it appears that the machine knows where an openable wall is."
he says, "Yet it doesn't show them on the display. It's almost like it was
designed this way to teach us something..." You hope you've learned the lesson,
as it looks like it's about to come in handy.
"""
from .framework import exercise
from random import randint

def user_func(walker):
    from ..solution.exercise6 import hand
    hand(walker)

def main():
    maze = [[14, 8, 11, 13, 13],
            [13, 4, 10, 0, 3],
            [4, 3, 14, 1, 13],
            [4, 10, 9, 4, 3],
            [7, 14, 3, 7, 15]]
    if randint(0, 1):
        maze[3][4] += 32
    else:
        maze[4][3] += 16
    exercise(user_func, fields=maze)
