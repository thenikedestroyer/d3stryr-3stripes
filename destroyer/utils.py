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


def get_random_user_agent():
    """
    Returns a random user-agent.
    """
    browsers = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
        'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53',
        'Mozilla/5.0 (iPad; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5',
        'Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true',
        'Mozilla/5.0 (Linux; U; en-us; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us; Silk/1.0.141.16-Gen4_11004310) AppleWebkit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true',
        'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; Nexus S Build/GRJ22) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; Android 4.3; Nexus 7 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.72 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
        'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+',
        'Mozilla/5.0 (Linux; Android 4.3; Nexus 10 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.72 Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 2.3; en-us; SAMSUNG-SGH-I717 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; Android 4.2.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 2.2; en-us; SCH-I800 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    ]
    return random.choice(browsers)


__all__ = ['d_', 's_', 'x_', 'z_', 'lb_', 'lr_', 'y_', 'o_', 'get_chromedriver', 'get_random_user_agent']
