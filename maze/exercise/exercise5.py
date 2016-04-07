"""As you recover from that last drop, the view outside the machine's windows
draws your attentions. You're surrounded by walls in all four directions.
Going out to examine the situation, you can see no way out. The walls are solid
and well constructed, not a crack or seam to be found. You resign yourself to
your eventual death from starvation.

Suddenly, one of the walls slides down into the floor, revealing a passage.
There's a shout of surprise from inside the machine. "My friend, come see this!"
Inside, Fulan is resting his hand on a metal panel, above which are some
characters you can't quite make out. "This panel was revealed after the last
drop." he says. "The writing above it says 'Say the magic words to pass.', so I
tried a few. It turned out to be 'Open Sesame', of all things." He shakes his
head. "These ruins are getting stranger and stranger."
"""
from .framework import exercise

def user_func(walker):
    from ..solution.exercise5 import hand
    hand(walker)

def main():
    maze = [[12, 10, 10, 10, 9],
            [4, 8, 10, 9, 5],
            [7, 4, 11, 5, 5],
            [12, 0, 11, 7, 7],
            [7, 6, 10, 27, 15]]
    exercise(user_func, fields=maze)

def register():
    return {'name': '2_classes', 'category': '2_Control_Structures'}
