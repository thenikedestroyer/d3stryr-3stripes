import json
import sys
import time

import requests

from settings import captcha_tokens, exit_code, hyped_skus, user_config
from utils import *
import inventory

# Disable urllib3 warnings
requests.packages.urllib3.disable_warnings()


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
