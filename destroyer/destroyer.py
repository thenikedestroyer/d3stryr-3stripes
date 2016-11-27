import json
import os
import random
import sys
import time
from datetime import datetime

import requests

from harvester import harvest_tokens_manually
from settings import exit_code, hypedSkus, captcha_tokens, user_config
from utils import *

# Disable urllib3 warnings
requests.packages.urllib3.disable_warnings()


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
                sys.exit(exit_code)
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
        'User-Agent': get_random_user_agent(),
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
        'User-Agent': get_random_user_agent(),
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
    captcha_tokens_reversed = []
    if user_config.manuallyHarvestTokens:
        harvest_tokens_manually()
        captcha_tokens_reversed = list(reversed(captcha_tokens))
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
                if captcha_tokens_reversed:
                    # Use a manual token
                    captchaToken = captcha_tokens_reversed.pop()
                    print (d_(), s_('Number of Tokens Left'),
                           lb_(len(captcha_tokens_reversed)))
                else:
                    # No manual tokens to pop - so lets use 2captcha
                    captchaToken = getACaptchaTokenFrom2Captcha()
            addToCartChromeAJAX(pid, captchaToken)
        except KeyboardInterrupt:
            print (d_(), x_('KeyboardInterrupt'))
            sys.exit(exit_code)
        except:
            print (d_(), x_('Add-To-Cart'), lr_(mySize, ' : ', 'Not Found'))


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
    browser = get_chromedriver(chrome_folder_location='ChromeFolder')
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
