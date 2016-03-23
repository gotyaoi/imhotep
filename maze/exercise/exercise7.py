"""As you lay on you back after the most recent drop, you hear a strange
grinding sound. On the display, you can see an opening moving up and down a
section of wall. As the machine starts up, the opening stops moving. A number
flashes on the screen.
"""
from .framework import exercise
from random import randint

def main():
    maze = [[14, 10, 10, 10, 11],
            [12, 10, 10, 10, 9],
            [5, 13, 14, 10, 3],
            [4, 2, 9, 12, 11],
            [6, 11, 6, 2, 11]]
    rand = randint(0, 4)
    maze[0][rand] &= 13
    maze[1][rand] &= 7
    def user_func(walker):
        from ..solution.exercise7 import hand
        hand(walker, rand)
    exercise(user_func, fields=maze)
