#!/usr/bin/env python3

import json
import sys

from cart import process_add_to_cart
from product import getProductInfo, printProductInfo
from settings import exit_code, user_config
from utils import d_, lr_, x_

if __name__ == '__main__':
    # Print the run parameters
    user_config.print_config()

    # Check for dumb asses
    if not user_config.validate_config():
        sys.stdout.flush()
        sys.exit(exit_code)

    # Get product info
    productInfo = getProductInfo()

    # Print product info
    printProductInfo(productInfo)

    # If product count is not zero process add to cart
    if productInfo['productCount'] > 0:
        process_add_to_cart(productInfo)
    elif productInfo['productCount'] == -1:
        print (d_(), x_('Variant Count'), lr_('-1'))
        process_add_to_cart(productInfo)
    else:
        print (d_(), x_('Variant Count'), lr_('0'))
