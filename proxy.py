"""
Credits of this code:
  Taken from this repo https://bitbucket.org/canassa/switch-proxy
  I just made it python3 compatible
"""

import _winreg as winreg
import configparser as ConfigParser
import ctypes
import os
import sys

WIN_PROXY = u'10.138.15.10:8080'
MERCURIAL_PROXY = u'http://87.254.212.121:8080'
ENV_HTTP_PROXY = MERCURIAL_PROXY


class Registry(object):
    def __init__(self, key_location, key_path):
        self.reg_key = winreg.OpenKey(key_location, key_path, 0, winreg.KEY_ALL_ACCESS)

    def set_key(self, name, value):
        try:
            _, reg_type = winreg.QueryValueEx(self.reg_key, name)
        except WindowsError:
            # If the value does not exists yet, we guess use a string as the
            # reg_type
            reg_type = winreg.REG_SZ
        winreg.SetValueEx(self.reg_key, name, 0, reg_type, value)

    def delete_key(self, name):
        try:
            winreg.DeleteValue(self.reg_key, name)
        except WindowsError:
            # Ignores if the key value doesn't exists
            pass


class WindowsProxy(Registry):
    # See http://msdn.microsoft.com/en-us/library/aa385328(v=vs.85).aspx
    # Causes the proxy data to be reread from the registry for a handle. No buffer
    # is required. This option can be used on the HINTERNET handle returned by
    # InternetOpen. It is used by InternetSetOption.
    INTERNET_OPTION_REFRESH = 37

    # Notifies the system that the registry settings have been changed so that it
    # verifies the settings on the next call to InternetConnect. This is used by
    # InternetSetOption.
    INTERNET_OPTION_SETTINGS_CHANGED = 39

    def __init__(self):
        super(WindowsProxy, self).__init__(winreg.HKEY_CURRENT_USER,
                                           r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
        self.internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

    def on(self):
        self.set_key('ProxyEnable', 1)
        self.set_key('ProxyOverride', u'*.local;<local>')  # Bypass the proxy for localhost
        self.set_key('ProxyServer', WIN_PROXY)

        self.refresh()

    def off(self):
        self.set_key('ProxyEnable', 0)

        self.refresh()

    def refresh(self):
        self.internet_set_option(0, self.INTERNET_OPTION_REFRESH, 0, 0)
        self.internet_set_option(0, self.INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)


class MercurialProxy(object):
    def __init__(self):
        self.mercurial_ini = os.path.join(os.path.expanduser('~'), 'Mercurial.ini')

        self.config = ConfigParser.ConfigParser()
        self.config.read(self.mercurial_ini)

    def on(self):
        try:
            self.config.add_section('http_proxy')
        except ConfigParser.DuplicateSectionError:
            pass

        self.config.set('http_proxy', 'host', MERCURIAL_PROXY)
        self.save()

    def off(self):
        try:
            self.config.remove_section('http_proxy')
        except ConfigParser.NoSectionError:
            pass
        self.save()

    def save(self):
        with open(self.mercurial_ini, 'wb') as updated_config:
            self.config.write(updated_config)


class EnvironmentVariables(Registry):
    """
    Configures the HTTP_PROXY environment variable, it's used by the PIP proxy
    """

    def __init__(self):
        super(EnvironmentVariables, self).__init__(winreg.HKEY_LOCAL_MACHINE,
                                                   r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')

    def on(self):
        self.set_key('HTTP_PROXY', ENV_HTTP_PROXY)
        self.refresh()

    def off(self):
        self.delete_key('HTTP_PROXY')
        self.refresh()

    def refresh(self):
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A

        #SendMessage = ctypes.windll.user32.SendMessageW
        #SendMessage(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u'Environment')

        SMTO_ABORTIFHUNG = 0x0002

        result = ctypes.c_long()
        SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
        SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u'Environment', SMTO_ABORTIFHUNG, 5000, ctypes.byref(result));


def on():
    print('Proxy enabled')
    WindowsProxy().on()
    MercurialProxy().on()
    EnvironmentVariables().on()


def off():
    print('Proxy disabled')
    WindowsProxy().off()
    MercurialProxy().off()
    EnvironmentVariables().off()


def exit_error(error):
    print(sys.stderr, error)
    exit(1)


def main():
    if len(sys.argv) != 2:
        exit_error('usage: ' + sys.argv[0] + ' [on|off]')
    {"on": on, "off": off}[sys.argv[1]]()


if __name__ == "__main__":
    main()