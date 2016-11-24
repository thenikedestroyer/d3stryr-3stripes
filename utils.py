import os
from datetime import datetime

from settings import revision


class Color:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'

    def __getattribute__(self, name):
        if 'nt' in os.name:
            # We remove ANSI coloring for Windows
            return ''
        return super().__getattribute__(name)


def d_(destroyer_id=None):
    """
    In a threaded setup you can identify a printed line by its threadId
    I just call it destroyerId
    """
    if destroyer_id is None:
        destroyer_id = revision

    timestamp = datetime.now()
    return 'Destroyer # {0:>4} {1:%I:%M:%S.%f}'.format(
        destroyer_id,
        datetime.now(),
    )[:-3]  # Cut the last 3 digits off milliseconds


def s_(*args):
    """
    Color for general values
    """
    input_string = ' '.join(map(str, args))
    return '{0}[{1:^21}]{2}'.format(
        Color.lightgrey,
        input_string,
        Color.reset,
    )


def x_(*args):
    """
    Color for exceptions
    """
    input_string = ' '.join(map(str, args))
    return '{0}[{1:^21}]{2}'.format(
        Color.lightred,
        input_string,
        Color.reset,
    )


def z_(*args):
    """
    Color for debugging
    """
    input_string = ' '.join(map(str, args))
    return '{0}[{1:^21}]{2}'.format(
        Color.orange,
        input_string,
        Color.reset,
    )


def lb_(*args):
    """
    Colorize text with lightblue
    """
    input_string = ' '.join(map(str, args))
    return Color.lightblue + str(input_string) + Color.reset


def lr_(*args):
    """
    Colorize text with lightred
    """
    input_string = ' '.join(map(str, args))
    return Color.lightred + str(input_string) + Color.reset


def y_(*args):
    """
    Colorize text with yellow
    """
    input_string = ' '.join(map(str, args))
    return Color.yellow + str(input_string) + Color.reset


def o_(*args):
    """
    Colorize text with orange
    """
    input_string = ' '.join(map(str, args))
    return Color.orange + str(input_string) + Color.reset

__all__ = ['d_', 's_', 'x_', 'z_', 'lb_', 'lr_', 'y_', 'o_']
