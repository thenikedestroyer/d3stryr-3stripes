"""
Credits of this code:
  Taken from this repo https://bitbucket.org/canassa/switch-proxy
  I just made it python3 compatible
"""

import winreg
import ctypes


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

    def __init__(self, ip, port):
        self.WIN_PROXY = u'{}:{}'.format(ip, port)
        super(WindowsProxy, self).__init__(winreg.HKEY_CURRENT_USER,
                                           r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
        self.internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

    def on(self):
        self.set_key('ProxyEnable', 1)
        self.set_key('ProxyOverride', u'*.local;<local>')  # Bypass the proxy for localhost
        self.set_key('ProxyServer', self.WIN_PROXY)

        self.refresh()

    def off(self):
        self.set_key('ProxyEnable', 0)

        self.refresh()

    def refresh(self):
        self.internet_set_option(0, self.INTERNET_OPTION_REFRESH, 0, 0)
        self.internet_set_option(0, self.INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
