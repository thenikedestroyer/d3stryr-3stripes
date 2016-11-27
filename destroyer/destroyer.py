#!/usr/bin/env python3

import json
import sys

from cart import process_add_to_cart
from product import get_product_info, print_product_info
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
    product_info = get_product_info()

    # Print product info
    print_product_info(product_info)

    # If product count is not zero process add to cart
    if product_info['productCount'] > 0:
        process_add_to_cart(product_info)
    elif product_info['productCount'] == -1:
        print (d_(), x_('Variant Count'), lr_('-1'))
        process_add_to_cart(product_info)
    else:
        print (d_(), x_('Variant Count'), lr_('0'))
