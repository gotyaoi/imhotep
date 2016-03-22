"""Exceptions used by this package.

WalkerStateError - Walker in a bad state.
BadCommand - A bad command was issued.
TooManyInstructions - Too many instructions were used.
Win - You can stop now.
"""

class WalkerStateError(Exception):
    """An Error for trying to make the Walker do something it's not ready for."""
    pass

class BadCommand(Exception):
    """An Error for a bad command in move's input."""
    pass

class TooManyInstructions(Exception):
    """An Exception to indicate that run has executed too many instructions."""
    pass

class Win(Exception):
    """An Exception to indicate that the win condition has been reached."""
    pass
