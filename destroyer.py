import json
import os
import random
import sys
import time
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from settings import exitCode, hypedSkus, user_config
from utils import *

# Disable urllib3 warnings
requests.packages.urllib3.disable_warnings()

def agent():
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


def getACaptchaTokenFrom2Captcha():
    session = requests.Session()
    session.verify = False
    session.cookies.clear()
    pageurl = 'http://www.%s' % user_config.marketDomain
    print (d_(), s_('pageurl'), lb_(pageurl))
    print (d_(), s_('sitekey'), lb_(user_config.sitekey))
    while True:
        data = {
            'key': user_config.apikey2captcha,
            'action': 'getbalance',
            'json': 1,
        }
        response = session.get(url='http://2captcha.com/res.php', params=data)
        try:
            JSON = json.loads(response.text)
        except:
            print (d_(), x_('Response'), y_(response.text))
            if "ERROR_WRONG_USER_KEY" in response.text:
                sys.exit(1)
            print (d_(), x_('Sleeping'), y_(user_config.sleeping, 'seconds'))
            time.sleep(user_config.sleeping)
            continue

        if JSON['status'] == 1:
            balance = JSON['request']
            print (d_(), s_('Balance'), lb_('${0}'.format(balance)))
        else:
            print (d_(), x_('Balance'))
        CAPTCHAID = None
        proceed = False
        while not proceed:
            data = {
                'key': user_config.apikey2captcha,
                'method': 'userrecaptcha',
                'googlekey': user_config.sitekey,
                'proxy': user_config.proxy2Captcha,
                'proxytype': 'HTTP',
                'pageurl': pageurl,
                'json': 1
            }
            response = session.post(
                url='http://2captcha.com/in.php', data=data)
            try:
                JSON = json.loads(response.text)
            except:
                print (d_(), x_('Response'), y_(response.text))
                print (d_(), x_('Sleeping'), y_(user_config.sleeping, 'seconds'))
                time.sleep(user_config.sleeping)
                continue

            if JSON['status'] == 1:
                CAPTCHAID = JSON['request']
                proceed = True
                print (d_(), s_('Captcha ID'), lb_(CAPTCHAID))
            else:
                print (d_(), x_('Response'), y_(response.text))
                print (d_(), x_('Sleeping'), y_(user_config.sleeping, 'seconds'))
                time.sleep(user_config.sleeping)
        print (d_(), s_('Waiting'), '%d seconds before polling for Captcha response' % user_config.sleeping)
        time.sleep(user_config.sleeping)
        TOKEN = None
        proceed = False
        while not proceed:
            data = {
                'key': user_config.apikey2captcha,
                'action': 'get',
                'json': 1,
                'id': CAPTCHAID,
            }
            response = session.get(url='http://2captcha.com/res.php', params=data)
            JSON = json.loads(response.text)
            if JSON['status'] == 1:
                TOKEN = JSON['request']
                proceed = True
                print (d_(), s_('Token ID'), lb_(TOKEN))
            else:
                print (d_(), x_('Response'), y_(response.text))
                print (d_(), x_('Sleeping'), y_(user_config.sleeping, 'seconds'))
                time.sleep(user_config.sleeping)
        data = {
            'key': user_config.apikey2captcha,
            'action': 'getbalance',
            'json': 1,
        }
        response = session.get(url='http://2captcha.com/res.php', params=data)
        JSON = json.loads(response.text)
        if JSON['status'] == 1:
            balance = JSON['request']
            print (d_(), s_('Balance'), lb_('${0}'.format(balance)))
        else:
            print (d_(), x_('Balance'))
        if TOKEN is not None:
            return TOKEN


def getClientResponse():
    headers = {
        'User-Agent': agent(),
    }
    session = requests.Session()
    session.verify = False
    session.cookies.clear()
    skus = ','.join(
        ['{sku}_{size_id}'.format(sku=user_config.masterPid, size_id=x)
         for x in range(510, 820, 10)])

    # Other countries will use US format like MX.
    # They can just request US value for parametersLocale in config.cfg
    if user_config.parametersLocale == 'US':
        clientStockURL = (
            'http://{0}-us-adidasgroup.demandware.net/s/adidas-{1}'
            '/dw/shop/v15_6/products/({2})'
            '?client_id={3}&expand=availability,variations,prices'
        ).format(user_config.apiEnv, user_config.marketLocale, skus, user_config.clientId,)
    else:
        clientStockURL = (
            'http://{0}-store-adidasgroup.demandware.net/s/adidas-{1}'
            '/dw/shop/v15_6/products/({2})'
            '?client_id={3}&expand=availability,variations,prices'
        ).format(user_config.apiEnv, user_config.marketLocale, skus, user_config.clientId,)
    if user_config.debug:
        print(d_(), z_('Debug'), o_(clientStockURL))

    response = session.get(url=clientStockURL, headers=headers)
    return response


def getVariantResponse():
    headers = {
        'User-Agent': agent(),
    }
    session = requests.Session()
    session.verify = False
    session.cookies.clear()

    # Not sure why I even bother making a case for Portugal if dude on twitter
    # keeps telling it doesnt work. Da fuq is MLT?
    if user_config.market == 'PT':
        variantStockURL = (
            'http://www.{0}/on/demandware.store/Sites-adidas-'
            '{1}-Site/MLT/Product-GetVariants?pid={2}'
        ).format(user_config.marketDomain, user_config.marketLocale, user_config.masterPid,)
    else:
        variantStockURL = (
            'http://www.{0}/on/demandware.store/Sites-adidas-'
            '{1}-Site/{2}/Product-GetVariants?pid={3}'
        ).format(user_config.marketDomain, user_config.marketLocale, user_config.market, user_config.masterPid,)

    if user_config.debug:
        print(d_(), z_('Debug'), o_(variantStockURL))
    response = session.get(url=variantStockURL, headers=headers)
    return response


def canonicalizeProductInfoClient(productJSON):
    # Initialize a dictionary.
    productInfo = {}
    productInfo['productStock'] = {}

    # Because of how we order the skus in clientStockURL 0-index is
    # always masterPid info in the JSON response.
    try:
        data = productJSON['data'][0]
    except:
        print(d_(), x_('Parse Client JSON'))
    try:
        productInfo['productName'] = data['name']
    except:
        productInfo['productName'] = '/'
    try:
        productInfo['productColor'] = data['c_defaultColor']
    except:
        productInfo['productColor'] = '/'
    try:
        productInfo['productOrderable'] = data['inventory']['orderable']
    except:
        productInfo['productOrderable'] = False
    try:
        productInfo['productPrice'] = data['price']
    except:
        productInfo['productPrice'] = 0
    try:
        productInfo['productCount'] = productJSON['count'] - 1
    except:
        productInfo['productCount'] = 0
    try:
        productInfo['productATS'] = data['inventory']['ats']
    except:
        productInfo['productATS'] = 0
    try:
        productInfo['productStockLevel'] = data['inventory']['stock_level']
    except:
        productInfo['productStockLevel'] = 0

    # Because data['c_sizeFTW'] and data['c_sizeSearchValue'] yield nonsense
    # for some EU locales:
    # Build a dictionary to convert adidas _XXX sizing to canonical sizing.
    adidasSize2Size = {}
    for variant in data['variation_attributes'][0]['values']:
        adidasSize2Size['{0}_{1}'.format(user_config.masterPid, variant['value'])] = variant['name']

    # We could avoid:
    # if data['id'] != masterPid:
    # by using a for loop to iterate through:
    # range(1,len(productJSON['data'])):
    # But I doubt there is a performance hit here. Because this is only done
    # once even if threading is introduce in the future.
    for data in productJSON['data']:
        if data['id'] != user_config.masterPid:
            try:
                productInfo['productStock'][adidasSize2Size[data['id']]] = {}
                productInfo['productStock'][adidasSize2Size[data['id']]][
                    'ATS'] = int(data['inventory']['ats'])
                productInfo['productStock'][adidasSize2Size[data['id']]]['pid'] = data['id']
            except:
                print(d_(), x_('Client Inventory'))

    if user_config.debug:
        print(d_(), z_('Debug'), o_(json.dumps(productInfo, indent=2)))
    return productInfo


def canonicalizeProductInfoVariant(productJSON):
    """
    Creating a standard format of the data representation using a dictionary
    """
    productInfo = {}
    productInfo['productStock'] = {}
    productInfo['productName'] = '/'
    productInfo['productColor'] = '/'
    productInfo['productOrderable'] = '/'
    try:
        productInfo['productPrice'] = productJSON[
            'variations']['variants'][0]['pricing']['standard']
    except:
        productInfo['productPrice'] = 0
    try:
        productInfo['productCount'] = len(productJSON['variations']['variants'])
    except:
        productInfo['productCount'] = 0

    productInfo['productATS'] = 0

    try:
        for variant in productJSON['variations']['variants']:
            productInfo['productATS'] = productInfo['productATS'] + int(variant['ATS'])
            productInfo['productStock'][variant['attributes']['size']] = {}
            productInfo['productStock'][variant['attributes']['size']]['ATS'] = int(variant['ATS'])
            productInfo['productStock'][variant['attributes']['size']]['pid'] = variant['id']
    except:
        print(d_(), x_('Variant Inventory'))

    productInfo['productStockLevel'] = productInfo['productATS']

    if user_config.debug:
        print(d_(), z_('Debug'), o_(json.dumps(productInfo, indent=2)))
    return productInfo


def getProductInfo():
    if user_config.useClientInventory:
        try:
            print(d_(), s_('Client Endpoint'))
            response = getClientResponse()
            productJSON = json.loads(response.text)
            productInfoClient = canonicalizeProductInfoClient(productJSON)
            return productInfoClient
        except:
            print(d_(), x_('Client Endpoint'))
            if user_config.debug:
                print(d_(), z_('Debug'),
                      o_('Client Endpoint Response -', response.text))
    # If we reached this point then useClientInventory didn't successfully
    # return. So lets proceed with useVariantInventory.
    try:
        print(d_(), s_('Variant Endpoint'))
        response = getVariantResponse()
        productJSON = json.loads(response.text)
        productInfoVariant = canonicalizeProductInfoVariant(productJSON)
        return productInfoVariant
    except:
        print(d_(), x_('Variant Endpoint'))
        if user_config.debug:
            print(d_(), z_('Debug'),
                  o_('Variant Endpoint Response -', response.text))
    # If we reached this point then useVariantInventory did not successfully
    # return. So lets produce at minimum size inventory.
    # We will refer to this as Fallback for productInfo (when both client and
    # variant produces no inventory result).
    productInfoFallback = {}
    productInfoFallback['productStock'] = {}
    productInfoFallback['productName'] = '/'
    productInfoFallback['productColor'] = '/'
    productInfoFallback['productOrderable'] = '/'
    productInfoFallback['productPrice'] = 0
    productInfoFallback['productCount'] = -1
    productInfoFallback['productATS'] = -1
    productInfoFallback['productStockLevel'] = -1
    # US vs EU sizing seems to be off by 0.5 size
    if user_config.parametersLocale == 'US':
        literalSize = 4.5
        for variant in range(540, 750, 10):
            stringLiteralSize = str(literalSize).replace('.0', '')
            productInfoFallback['productStock'][stringLiteralSize] = {}
            productInfoFallback['productStock'][stringLiteralSize]['ATS'] = 1
            productInfoFallback['productStock'][stringLiteralSize][
                'pid'] = '{0}_{1}'.format(user_config.masterPid, variant)
            literalSize = literalSize + .5
    else:
        literalSize = 4.5
        for variant in range(550, 750, 10):
            stringLiteralSize = str(literalSize).replace('.0', '')
            productInfoFallback['productStock'][stringLiteralSize] = {}
            productInfoFallback['productStock'][stringLiteralSize]['ATS'] = 1
            productInfoFallback['productStock'][stringLiteralSize][
                'pid'] = '{0}_{1}'.format(user_config.masterPid, variant)
            literalSize = literalSize + .5
    return productInfoFallback


def printProductInfo(productInfo):
    print(d_(), s_('Product Name'), lb_(productInfo['productName']))
    print(d_(), s_('Product Color'), lb_(productInfo['productColor']))
    print(d_(), s_('Price'), lb_(productInfo['productPrice']))
    print(d_(), s_('Orderable'), lb_(productInfo['productOrderable']))
    print(d_(), s_('ATS'), lb_(str(productInfo['productATS']).rjust(6, ' ')))
    print(d_(), s_('Stock Level'),
          lb_(str(productInfo['productStockLevel']).rjust(6, ' ')))
    print(d_(), s_('Size Inventory'))
    for size in sorted(productInfo['productStock']):
        print(d_(), s_(size.ljust(5, ' '), '/',
                       productInfo['productStock'][size]['pid']),
              lb_(str(productInfo['productStock'][size]['ATS']).rjust(6, ' ')))


def processAddToCart(productInfo):
    captchaTokensReversed = []
    if user_config.manuallyHarvestTokens:
        harvestTokensManually()
        for index in range(0, len(captchaTokens)):
            captchaTokensReversed.append(captchaTokens.pop())
    for mySize in user_config.mySizes:
        try:
            mySizeATS = productInfo['productStock'][mySize]['ATS']
            if mySizeATS == 0:
                print (d_(), x_('Add-To-Cart'), lr_('Out of Stock:', mySize))
                continue
            print (d_(), s_('Add-To-Cart'), mySize, ':', str(mySizeATS))
            pid = productInfo['productStock'][mySize]['pid']

            # Check if we need to process captcha
            captchaToken = ''
            if user_config.processCaptcha:
                # See if we have any manual tokens available
                if len(captchaTokensReversed) > 0:
                    # Use a manual token
                    captchaToken = captchaTokensReversed.pop()
                    print (d_(), s_('Number of Tokens Left'),
                           lb_(len(captchaTokensReversed)))
                else:
                    # No manual tokens to pop - so lets use 2captcha
                    captchaToken = getACaptchaTokenFrom2Captcha()
            addToCartChromeAJAX(pid, captchaToken)
        except KeyboardInterrupt:
            print (d_(), x_('KeyboardInterrupt'))
            sys.exit(exitCode)
        except:
            print (d_(), x_('Add-To-Cart'), lr_(mySize, ' : ', 'Not Found'))


def getChromeDriver(chromeFolderLocation=None, windowSize=None):
    chromedriver = None
    if 'nt' in os.name:
        # Es ventanas?
        if os.path.isfile('chromedriver.exe'):
            # Lets check to see if chromedriver.exe is in the current directory
            chromedriver = 'chromedriver.exe'
        elif os.path.isfile('C:\Windows\chromedriver.exe'):
            # Lets check to see if chromedriver.exe is in C:\Windows
            chromedriver = 'C:\Windows\chromedriver.exe'
        else:
            # Lets see if the end-user will read this and fix their own
            # problem before tweeting
            print (d_(), x_('Chromedriver.exe'),
                   lr_('was not found in the current folder or C:\Windows'))
            sys.stdout.flush()
            sys.exit(exitCode)
    else:
        # Es manzanas?
        if os.path.isfile('./chromedriver'):
            # Chromedriver should be in the current directory
            chromedriver = './chromedriver'
        else:
            print (d_(), x_('chromedriver'),
                   lr_('was not found in the current folder.'))
            sys.stdout.flush()
            sys.exit(exitCode)
    os.environ['webdriver.chrome.driver'] = chromedriver
    chrome_options = Options()

    # We store the browsing session in ChromeFolder so we can manually
    # delete it if necessary
    if chromeFolderLocation is not None:
        chrome_options.add_argument('--user-data-dir=' + chromeFolderLocation)

    if windowSize is not None:
        chrome_options.add_argument("window-size=" + windowSize[0])

    driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
    return driver


def addToCartChromeAJAX(pid, captchaToken):
    cookieScript = ''
    cookieScriptDomainAware = ''
    if user_config.marketLocale == 'PT':
        baseADCUrl = (
            'http://www.{0}/on/demandware.store/Sites-adidas-MLT-Site/{1}'
        ).format(user_config.marketDomain, user_config.market)
    else:
        baseADCUrl = (
            'http://www.{0}/on/demandware.store/Sites-adidas-{1}-Site/{2}'
        ).format(user_config.marketDomain, user_config.marketLocale, user_config.market)

    atcURL = baseADCUrl + '/Cart-MiniAddProduct'
    cartURL = baseADCUrl.replace('http://', 'https://') + '/Cart-Show'
    data = {}

    # If we are processing captcha then add to our payload.
    if user_config.processCaptcha:
        data['g-recaptcha-response'] = captchaToken

    # If we need captcha duplicate then add to our payload.
    if user_config.processCaptchaDuplicate:
        # Alter the atcURL for the captcha duplicate case
        atcURL = atcURL + '?clientId=' + user_config.clientId
        # Add captcha duplicate  to our payload.
        data[user_config.duplicateField] = captchaToken

    # If cookies need to be set then add to our payload.
    if 'neverywhere' not in user_config.cookies:
        cookieScript = 'document.cookie="{0}domain=.adidas.com;path=/";'.format(user_config.cookies)
        cookieScriptDomainAware = 'document.cookie="{0}domain=.{1};path=/";'.format(
            user_config.cookies, user_config.marketDomain)

    data['masterPid'] = user_config.masterPid
    data['pid'] = pid
    data['Quantity'] = '1'
    data['request'] = 'ajax'
    data['responseformat'] = 'json'
    data['sessionSelectedStoreID'] = 'null'
    script = """
      $.ajax({
        url: '""" + atcURL + """',
        data: """ + json.dumps(data, indent=2) + """,
        method: 'POST',
        crossDomain: true,
        contentType: 'application/x-www-form-urlencoded',
        xhrFields: {
            withCredentials: true
        },
        complete: function(data, status, xhr) {
          console.log(status);
          console.log(data);
        }
      });"""

    if user_config.useInjectionMethod:
        injectionURL = baseADCUrl + '/Cart-MiniAddProduct' + \
            '?pid=' + pid + '&masterPid=' + user_config.masterPid + '&ajax=true'
        if user_config.processCaptcha:
            injectionURL = injectionURL + '&g-recaptcha-response=' + captchaToken
        script = """
        var url='""" + injectionURL + """';
        document.getElementById(document.querySelector("[id^='dwfrm_cart']").id).action = url;
        document.getElementById(document.querySelector("[id^='dwfrm_cart']").id).submit();
      """

    externalScript = None
    if len(user_config.scriptURL) > 0 and '.js' in user_config.scriptURL:
        externalScript = """
            $.ajax({
              url: '""" + user_config.scriptURL + """',
              dataType: "script"
            });"""
    if user_config.debug:
        print(d_(), z_('Debug:data'), o_(json.dumps(data, indent=2)))
        print(d_(), z_('Debug:script'), o_(script))
        print(d_(), z_('Debug:cookie'), o_(cookieScript))
        print(d_(), z_('Debug:cookie'), o_(cookieScriptDomainAware))
        print(d_(), z_('Debug:external'), o_(externalScript))
    browser = getChromeDriver(chromeFolderLocation='ChromeFolder')
    browser.delete_all_cookies()
    if user_config.useInjectionMethod:
        browser.get(cartURL)
    else:
        browser.get(baseADCUrl)
    if len(cookieScript) > 0 and 'neverywhere' not in user_config.cookies:
        print (d_(), s_('Cookie Script'))
        browser.execute_script(cookieScript)
        browser.execute_script(cookieScriptDomainAware)
    if len(user_config.scriptURL) > 0 and '.js' in user_config.scriptURL:
        print (d_(), s_('External Script'))
        browser.execute_script(externalScript)
    print (d_(), s_('ATC Script'))
    browser.execute_script(script)
    # time.sleep(user_config.sleeping)
    browser.get(baseADCUrl + '/Cart-ProductCount')
    html_source = browser.page_source
    productCount = browser.find_element_by_tag_name('body').text
    productCount = productCount.replace('"', '')
    productCount = productCount.strip()
    if user_config.debug:
        print(d_(), z_('Debug'), o_('Product Count: %s' % productCount))
        print(d_(), z_('Debug'), o_('\n{0}'.format(html_source)))
    if (len(productCount) == 1) and (int(productCount) > 0):
        results = browser.execute_script('window.location="{0}"'.format(
            cartURL))
        temp = input('Press Enter to Close the Browser & Continue')
    else:
        print (d_(), x_('Product Count'), lr_(productCount))

    # Maybe the Product Count source has changed and we are unable
    # to parse correctly.
    if user_config.pauseBeforeBrowserQuit:
        temp = input('Press Enter to Close the Browser & Continue')

    # Need to delete all the cookes for this session or else we will have the
    # previous size in cart
    browser.delete_all_cookies()
    browser.quit()
    return


def activateCaptcha(driver):
    """
    Activate the catpcha widget
    """
    iframe = driver.find_element_by_css_selector('iframe[src*="api2/anchor"]')
    driver.switch_to_frame(iframe)
    try:
        CheckBox = WebDriverWait(driver, user_config.sleeping).until(
            expected_conditions.presence_of_element_located(
                (By.ID, 'recaptcha-anchor')))
    except:
        try:
            CheckBox = WebDriverWait(driver, user_config.sleeping).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, 'recaptcha-anchor')))
        except:
            print (d_(), x_('Activate Captcha'),
                   lr_('Failed to find checkbox'))
    CheckBox.click()


def checkSolution(driver, mainWindow):
    """
    Check to see if we solved the captcha
    """
    solved = False
    while not solved:
        driver.switch_to.window(mainWindow)
        try:
            iframe = driver.find_element_by_css_selector(
                'iframe[src*="api2/anchor"]')
        except:
            print (d_(), x_('Check Solution'), lr_('Failed to find checkbox'))
            return
        driver.switch_to_frame(iframe)
        try:
            temp = driver.find_element_by_xpath('//span[@aria-checked="true"]')
            print (d_(), s_('Check Solution'), lb_('Solved'))
            solved = True
        except:
            solved = False
        time.sleep(1)
    return solved


def getToken(driver, mainWindow):
    """
    We parse the token from the page
    """
    token = None
    driver.switch_to.window(mainWindow)
    try:
        Submit = WebDriverWait(driver, user_config.sleeping).until(
            expected_conditions.presence_of_element_located((By.ID, 'submit')))
        Submit.click()
        time.sleep(1)
    except:
        print (d_(), x_('Captcha Submit'), lr_('Failed to click submit'))

    tokenElement = driver.find_element_by_css_selector('p#token')
    token = tokenElement.get_attribute('value')
    if token is not None:
        print (d_(), s_('Get Token'), lb_(token))
    return token


def harvestTokensManually():
    print (d_(), s_('Manual Token Harvest'),
           lb_('Number of tokens harvested: %d' % len(captchaTokens)))

    # We will create the harvest.php on the fly based on locale and sitekey
    # values in config.cfg
    htmlSource = """
        <?php
         $siteKey = '""" + user_config.sitekey + """';
         $lang = 'en';
        ?>
         <?php if (isset($_POST['g-recaptcha-response'])): ?>
        <html>
         <head>
           <title>adidas Official Website | adidas</title>
         </head>
         <body>
         <?php $token=$_POST['g-recaptcha-response']; ?>
             <p id="token" value="<?php echo $token; ?>"
               style="padding: 3px; word-break: break-all;
                 word-wrap: break-word;"><?php echo $token; ?></p>
         <?php else: ?>
        <html>
         <head>
           <title>d3stryr 3stripes Manual Token Harvesting | adidas</title>
                <style type="text/css">
                    body {
                        margin: 1em 5em 0 5em;
                        font-family: sans-serif;
                    }
                    fieldset {
                        display: inline;
                        padding: 1em;
                    }
                </style>
         </head>
         <body>
            <p>Token Harvesting</p>
            <form action="/harvest.php" method="post">
                <fieldset>
                    <div class="g-recaptcha"
                      data-sitekey="<?php echo $siteKey; ?>"></div>
                    <script type="text/javascript"
                      src="https://www.google.com/recaptcha/api.js">
                    </script>
                    <p><input type="submit" value="Submit" id="submit"/></p>
                </fieldset>
            </form>
         <?php endif; ?>
         </body>
        </html>"""
    with open('harvest.php', 'w') as htmlFile:
        htmlFile.write(htmlSource)
    windowSize = ["640,640"]
    browser = getChromeDriver(
        chromeFolderLocation='ChromeTokenHarvestFolder', windowSize=windowSize)
    url = 'http://' + user_config.harvestDomain + ':' + user_config.phpServerPort + '/harvest.php'
    while len(captchaTokens) < user_config.numberOfTokens:
        browser.get(url)
        mainWindow = browser.current_window_handle
        try:
            activateCaptcha(driver=browser)
        except:
            print (d_(), x_('Page Load Failed'),
                   lr_('Did you launch the PHP server?'))
            print (d_(), x_('Page Load Failed'),
                   lr_('Falling back to 2captcha'))
            browser.quit()
            return
        solved = checkSolution(driver=browser, mainWindow=mainWindow)
        token = getToken(driver=browser, mainWindow=mainWindow)
        if token is not None:
            if len(captchaTokens) == 0:
                startTime = time.time()
            captchaTokens.append(token)
            print (d_(), s_('Token Added'))
            print (d_(), s_('Manual Token Harvest'),
                   lb_('Number of tokens harvested: %d' % len(captchaTokens)))
        currentTime = time.time()
        elapsedTime = currentTime - startTime
        print (d_(), s_('Total Time Elapsed'),
               lb_(str(round(elapsedTime, 2)), 'seconds'))
    browser.quit()
