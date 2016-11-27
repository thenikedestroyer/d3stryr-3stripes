import configparser
import os

from utils import d_, lb_, lr_, s_, z_

# Lets try to keep a revision tracking via commit number.
revision = 'c+137'

# Set this for parameters checking.
hyped_skus = ['BY9612', 'BY1605', 'BY9611']

# Code to indicate a shitty exit from the script.
exit_code = 1

# Store manually harvested captcha tokens here.
captcha_tokens = []

# Get the project directory to avoid using relative paths
PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))

# Parse configuration file
c = configparser.ConfigParser()
configFilePath = os.path.join(PROJECT_ROOT_DIR, 'config.cfg')
c.read(configFilePath)


class Config:
    # Pull user info for masterPid
    masterPid = c.get('cart', 'masterPid')

    # Get the size array
    mySizes = [size.strip() for size in c.get('cart', 'mySizes').split(',')]

    # Get product type
    isYeezyProduct = c.getboolean('cart', 'isYeezyProduct')

    # Pull user info for locale
    marketLocale = c.get('locale', 'marketLocale')
    parametersLocale = c.get('locale', 'parametersLocale')

    # Pull info based on marketLocale
    market = c.get('market', marketLocale)
    marketDomain = c.get('marketDomain', marketLocale)

    # Pull info based on parametersLocale
    if isYeezyProduct:
        apiEnv = c.get('clientId_Yeezy', 'apiEnv')
        clientId = c.get('clientId_Yeezy', parametersLocale)
        sitekey = c.get('sitekey_Yeezy', parametersLocale)
    else:
        apiEnv = c.get('clientId', 'apiEnv')
        clientId = c.get('clientId', parametersLocale)
        sitekey = c.get('sitekey', parametersLocale)

    # Pull 2captcha info
    proxy2Captcha = c.get('captcha', 'proxy2Captcha')
    apikey2captcha = c.get('captcha', 'apikey2captcha')

    # Pull run parameters for handing captchas
    processCaptcha = c.getboolean('captcha', 'processCaptcha')
    processCaptchaDuplicate = c.getboolean('captcha', 'processCaptchaDuplicate')

    # Pull run parameters for handing inventory endpoints
    useClientInventory = c.getboolean('inventory', 'useClientInventory')
    useVariantInventory = c.getboolean('inventory', 'useVariantInventory')

    # Pull atc parameters to determine if we use the injection method
    useInjectionMethod = c.getboolean('atc', 'useInjectionMethod')

    # Pull responseformat settings
    useResponseFormatJSON = c.getboolean('atc', 'useResponseFormatJSON')

    # Token Harvesting info
    manuallyHarvestTokens = c.getboolean('harvest', 'manuallyHarvestTokens')
    numberOfTokens = c.getint('harvest', 'numberOfTokens')
    harvestDomain = c.get('harvest', 'harvestDomain')

    # Pull info necessary for a Yeezy drop
    duplicateField = c.get('duplicate', 'duplicate')
    cookies = c.get('cookie', 'cookie')

    # Just incase we nee to run an external script.
    scriptURL = c.get('script', 'scriptURL')

    # Pull the amount of time to sleep in seconds when needed
    sleeping = c.getint('sleeping', 'sleeping')

    # Are we debugging?
    debug = c.getboolean('debug', 'debug')

    # Under development
    pollProductPageForSiteKey = c.getboolean('development', 'pollProductPageForSiteKey')
    useOnlyProductPageSiteKey = c.getboolean('development', 'useOnlyProductPageSiteKey')

    # Require end-user to press enter before terminating Chrome's browser window during ATC
    pauseBeforeBrowserQuit = c.getboolean('debug', 'pauseBeforeBrowserQuit')

    def __init__(self, *args, **kwargs):
        # Because end-users refuse to read and understand the config.cfg file lets go
        # ahead and set processCaptcha to True if harvest is turned on.
        if self.manuallyHarvestTokens:
            self.processCaptcha = True

    def print_config(self):
        """
        Print out config for debugging.
        """
        print(d_(), s_('Market Locale'), lb_(self.marketLocale))
        print(d_(), s_('Parameters Locale'), lb_(self.parametersLocale))
        print(d_(), s_('Market'), lb_(self.market))
        print(d_(), s_('Market Domain'), lb_(self.marketDomain))
        print(d_(), s_('API Environment'), lb_(self.apiEnv))
        print(d_(), s_('Market Client ID'), lb_(self.clientId))
        print(d_(), s_('Market Site Key'), lb_(self.sitekey))
        print(d_(), s_('Captcha Duplicate'), lb_(self.duplicateField))
        print(d_(), s_('Cookie'), lb_(self.cookies))
        print(d_(), s_('Process Captcha'), lb_(self.processCaptcha))
        print(d_(), s_('Use Duplicate'), lb_(self.processCaptchaDuplicate))
        print(d_(), s_('Product ID'), lb_(self.masterPid))
        print(d_(), s_('Desired Size'), lb_(self.mySizes))
        print(d_(), s_('Manual Token Harvest'), lb_(self.manuallyHarvestTokens))
        print(d_(), s_('Tokens to Harvest'), lb_(self.numberOfTokens))
        print(d_(), s_('Harvest Domain'), lb_(self.harvestDomain))
        print(d_(), s_('Sleeping'), lb_(self.sleeping))
        print(d_(), s_('Debug'), lb_(self.debug))
        print(d_(), s_('External Script URL'), lb_(self.scriptURL))
        print(d_(), s_('Pause Between ATC'), lb_(self.pauseBeforeBrowserQuit))
        print(d_(), s_('Use Link Injection'), lb_(self.useInjectionMethod))

    def validate_config(self):
        """
        Validate the user-set config.
        """
        nah = False
        if self.marketLocale == 'US' and self.parametersLocale != 'US':
            print(d_(), z_('config.cfg'), lr_('Invalid marketLocale and parametersLocale combination.'))
            nah = True

        if self.useClientInventory and self.useVariantInventory:
            print(d_(), z_('config.cfg'), lr_('You should not set both inventory methods to True.'))

        if not self.manuallyHarvestTokens:
            # User is not token harvesting
            if self.processCaptcha:
                if self.apikey2captcha == 'xXx':
                    print(d_(), z_('config.cfg'),
                          lr_('You need a valid apikey2captcha if you '
                              'want to use 2captcha service! Visit 2captcha.com'))
                    nah = True
                if self.proxy2Captcha == 'localhost':
                    print(d_(), z_('config.cfg'),
                          lr_('Unless you are testing - you should consider '
                              'providing an IP whitelisted proxy for 2captcha to use.'))
        else:
            # User is token harvesting
            if not self.processCaptcha:
                # This should have been automatically set in the printRunParameters
                # but lets check.
                print(d_(), z_('config.cfg'),
                      lr_('You want to manually harvest tokens but you have not set processCaptcha to True. '
                          'Much reading you have done.'))
                nah = True
            if self.numberOfTokens < 1:
                print(d_(), z_('config.cfg'),
                      lr_('Your config.cfg makes no fucking sense. Why is numberOfTokens set to zero? '
                          'And why are you requesting to harvest tokens?'))
                nah = True
            if self.numberOfTokens > 5:
                print(d_(), z_('config.cfg'), '',
                      lr_('You requested to harvest a large number of tokens. '
                          'You wont be able to ATC until after you harvest all '
                          'of the tokens. And tokens have a lifespan of ~ '
                          '120 seconds.'))

        if self.sleeping < 3:
            print(d_(), z_('config.cfg'),
                  lr_('Your sleeping value is less than 3 seconds. It might not offer enough time between events.'))
        if self.masterPid in str(hyped_skus):
            if not self.processCaptchaDuplicate:
                print(d_(), z_('config.cfg'), lr_('This item is likely to make use of a captcha duplicate.'))
            if 'neverywhere' in self.cookies:
                print(d_(), z_('config.cfg'), lr_('This item is likely to make use of a cookie.'))
        if not self.debug:
            print(d_(), z_('config.cfg'),
                  lr_('debug is turned off. If you run into any issues dont bother tweeting them to me. '
                      'Because I will ask you why debug is turned off.'))

        return not nah

# This is our config instance.
user_config = Config()
