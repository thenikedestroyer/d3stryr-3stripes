import json
import sys
import time

import requests

from jinja2 import Environment, PackageLoader

from autocaptcha import get_token_from_2captcha
from harvester import harvest_tokens_manually
from settings import captcha_tokens, exit_code, hypedSkus, user_config
from utils import *
import inventory

# Disable urllib3 warnings
requests.packages.urllib3.disable_warnings()

# Define template environment for Jinja2 templates
jinja_env = Environment(loader=PackageLoader('destroyer', 'templates'))


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
            response = inventory.get_client_response()
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
        response = inventory.get_variant_response()
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
                    captchaToken = get_token_from_2captcha()
            add_to_cart_chrome_ajax(pid, captchaToken)
        except KeyboardInterrupt:
            print (d_(), x_('KeyboardInterrupt'))
            sys.exit(exit_code)
        except:
            raise
            print (d_(), x_('Add-To-Cart'), lr_(mySize, ' : ', 'Not Found'))


def add_to_cart_chrome_ajax(pid, captcha_token):
    cookie_script = ''
    cookie_script_domain_aware = ''
    if user_config.marketLocale == 'PT':
        base_atc_url = (
            'http://www.{0}/on/demandware.store/Sites-adidas-MLT-Site/{1}'
        ).format(user_config.marketDomain, user_config.market)
    else:
        base_atc_url = (
            'http://www.{0}/on/demandware.store/Sites-adidas-{1}-Site/{2}'
        ).format(user_config.marketDomain, user_config.marketLocale, user_config.market)

    atc_url = '{0}/Cart-MiniAddProduct'.format(base_atc_url)
    cart_url = base_atc_url.replace('http://', 'https://') + '/Cart-Show'
    data = {
        'masterPid': user_config.masterPid,
        'pid': pid,
        'Quantity': '1',
        'request': 'ajax',
        'responseformat': 'json',
        'sessionSelectedStoreID': 'null',
    }

    # If we are processing captcha then add to our payload.
    if user_config.processCaptcha:
        data['g-recaptcha-response'] = captcha_token

    # If we need captcha duplicate then add to our payload.
    if user_config.processCaptchaDuplicate:
        # Alter the ATC URL for the captcha duplicate case
        atc_url = '{0}?clientId={1}'.format(atc_url, user_config.clientId)
        # Add captcha duplicate  to our payload.
        data[user_config.duplicateField] = captcha_token

    # If cookies need to be set then add to our payload.
    if 'neverywhere' not in user_config.cookies:
        cookie_script = 'document.cookie="{0}domain=.adidas.com;path=/";'.format(user_config.cookies)
        cookie_script_domain_aware = 'document.cookie="{0}domain=.{1};path=/";'.format(
            user_config.cookies, user_config.marketDomain)

    # Render the ATC script
    script = jinja_env.get_template('atc_script.js').render(atc_url=atc_url, data=json.dumps(data, indent=2))

    if user_config.useInjectionMethod:
        injection_url = '{0}/Cart-MiniAddProduct?pid={1}&masterPid={2}&ajax=true'.format(
            base_atc_url, pid, user_config.masterPid)
        if user_config.processCaptcha:
            injection_url += '&g-recaptcha-response={0}'.format(captcha_token)

        # Render the injection script
        script = jinja_env.get_template('injection_script.js').render(injection_url=injection_url)

    external_script = None
    if len(user_config.scriptURL) > 0 and '.js' in user_config.scriptURL:
        # Render the external script
        external_script = jinja_env.get_template('external_script.js').render(script_url=user_config.scriptURL)
    if user_config.debug:
        print(d_(), z_('Debug:data'), o_(json.dumps(data, indent=2)))
        print(d_(), z_('Debug:script'), o_(script))
        print(d_(), z_('Debug:cookie'), o_(cookie_script))
        print(d_(), z_('Debug:cookie'), o_(cookie_script_domain_aware))
        print(d_(), z_('Debug:external'), o_(external_script))
    browser = get_chromedriver(chrome_folder_location='ChromeFolder')
    browser.delete_all_cookies()
    if user_config.useInjectionMethod:
        browser.get(cart_url)
    else:
        browser.get(base_atc_url)
    if len(cookie_script) > 0 and 'neverywhere' not in user_config.cookies:
        print (d_(), s_('Cookie Script'))
        browser.execute_script(cookie_script)
        browser.execute_script(cookie_script_domain_aware)
    if len(user_config.scriptURL) > 0 and '.js' in user_config.scriptURL:
        print (d_(), s_('External Script'))
        browser.execute_script(external_script)
    print (d_(), s_('ATC Script'))
    browser.execute_script(script)
    # time.sleep(user_config.sleeping)
    browser.get(base_atc_url + '/Cart-ProductCount')
    html_source = browser.page_source
    product_count = browser.find_element_by_tag_name('body').text.replace('"', '').strip()

    if user_config.debug:
        print(d_(), z_('Debug'), o_('Product Count: %s' % product_count))
        print(d_(), z_('Debug'), o_('\n{0}'.format(html_source)))
    if len(product_count) == 1 and int(product_count) > 0:
        results = browser.execute_script('window.location="{0}"'.format(cart_url))
        input('Press Enter to Close the Browser & Continue')
    else:
        print (d_(), x_('Product Count'), lr_(product_count))

    # Maybe the Product Count source has changed and we are unable
    # to parse correctly.
    if user_config.pauseBeforeBrowserQuit:
        input('Press Enter to Close the Browser & Continue')

    # Need to delete all the cookes for this session or else we will have the
    # previous size in cart
    browser.delete_all_cookies()
    browser.quit()
