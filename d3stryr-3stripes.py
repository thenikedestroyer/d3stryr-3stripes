#!/usr/bin/env python3
#Import from site-packages
import json
#Imports from destroyer.py
from destroyer import d_,x_,lr_
from destroyer import printRunParameters
from destroyer import getProductInfo
from destroyer import printProductInfo
from destroyer import processAddToCart

if __name__ == "__main__":
  #Print the run parameters
  printRunParameters()
  #Get product info
  productInfo=getProductInfo()
  #Print product info
  printProductInfo(productInfo)
  #If product count is not zero process add to cart
  if productInfo["productCount"] > 0:
    processAddToCart(productInfo)
  elif productInfo["productCount"] == -1:
    print (d_()+x_("Variant Count")+lr_("-1"))
    processAddToCart(productInfo)
  else:
    print (d_()+x_("Variant Count")+lr_("0"))
