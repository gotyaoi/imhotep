# In this exercise don't worry about this line for now.
def hand(walker):
    # In python being indented like this is called being inside a block. Make
    # sure anything you write in this exercise is indented by 4 spaces.

    # In this exercise, one of the eastern walls of this corridor is openable,
    # but which one it is is randomized each time you run the exercise. You
    # could write a bunch of if statements to check each one, but there's a more
    # concise way.

    # The while statement is sort of like the if statement, but with a twist.
    # Like the if statement, the block inside the while statement is only run if
    # the thing the while statement is checking is True. However, when the end
    # of the while statement's block is reached, it goes back to the top and
    # checks the condition again. If the condition is still True, it runs the
    # block again. It does this until the condition is False.

    # while somevariable:
    #    do_stuff()

    # Now, because the open_sesame method returns a True list when it opens a
    # wall, this is sort of the opposite of what we want, to exit the while
    # statement when a wall is opened. You can use "not" to reverse the True or
    # False that an if or while is checking.

    # while not somevariable:
    #     do_stuff()

    # Finally you may want to use a variable to keep track of how far up the
    # corridor you've gone, so you can tell how far back to go. You can then use
    # this variable in the instruction list you pass to run.
    pass
