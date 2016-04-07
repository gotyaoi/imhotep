"""A long corridor stretches out before you with no turns. The display of the
machine, however, shows more of the maze just on the other side of the wall. It
seems that the magic words are needed here, but where? Individually testing each
inch of the wall seems pretty tedious...
"""
from .framework import exercise
from random import randint

def user_func(walker):
    from ..solution.exercise8 import hand
    hand(walker)

def main():
    maze = [[14, 10, 10, 10, 11],
            [12, 10, 10, 10, 9],
            [5, 13, 14, 10, 3],
            [4, 2, 9, 12, 11],
            [6, 11, 6, 2, 11]]
    maze[0][randint(0, 4)] += 32
    exercise(user_func, fields=maze)

def register():
    return {'name': '5_while', 'category': '2_Control_Structures'}
