import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
    from settings import revision  # Avoid circular imports
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


def get_chromedriver(chrome_folder_location=None, window_size=None):
    from settings import exit_code  # Avoid circular imports
    chromedriver = None
    if 'nt' in os.name:
        # Es ventanas?
        if os.path.isfile('../bin/chromedriver.exe'):
            # Lets check to see if chromedriver.exe is in the current directory
            chromedriver = '../bin/chromedriver.exe'
        elif os.path.isfile('C:\Windows\chromedriver.exe'):
            # Lets check to see if chromedriver.exe is in C:\Windows
            chromedriver = 'C:\Windows\chromedriver.exe'
        else:
            # Lets see if the end-user will read this and fix their own
            # problem before tweeting
            print (d_(), x_('Chromedriver.exe'), lr_('was not found in the current folder or C:\Windows'))
            sys.stdout.flush()
            sys.exit(exit_code)
    else:
        # Es manzanas?
        if os.path.isfile('../bin/chromedriver'):
            # Chromedriver should be in the current directory
            chromedriver = '../bin/chromedriver'
        else:
            print (d_(), x_('chromedriver'), lr_('was not found in the current folder.'))
            sys.stdout.flush()
            sys.exit(exit_code)
    os.environ['webdriver.chrome.driver'] = chromedriver
    chrome_options = Options()

    # We store the browsing session in ChromeFolder so we can manually delete it if necessary
    if chrome_folder_location is not None:
        chrome_options.add_argument('--user-data-dir={0}'.format(chrome_folder_location))

    if window_size is not None:
        chrome_options.add_argument("window-size=" + window_size[0])

    return webdriver.Chrome(chromedriver, chrome_options=chrome_options)


__all__ = ['d_', 's_', 'x_', 'z_', 'lb_', 'lr_', 'y_', 'o_', 'get_chromedriver']
