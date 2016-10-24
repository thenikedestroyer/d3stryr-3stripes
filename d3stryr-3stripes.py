#!/usr/bin/env python3

import configparser
import json

from destroyer import d_,s_,x_,lb_,lr_,y_
from destroyer import getACaptchaToken
from destroyer import getClientResponse
from destroyer import getVariantResponse
from destroyer import canonicalizeProductInfoClient
from destroyer import canonicalizeProductInfoVariant
from destroyer import printProductInfo
from destroyer import addToCart

if __name__ == "__main__":

  config = configparser.ConfigParser()
  configFilePath = "config.cfg"
  config.read(configFilePath)

  marketLocale=config.get("user","marketLocale")
  parametersLocale=config.get("user","parametersLocale")
  masterPid=config.get("user","masterPid")
  mySizes=config.get("user","mySizes").replace(" ","").split(",")
  proxy2Captcha=config.get("user","proxy2Captcha")
  apikey2captcha=config.get("user","apikey2captcha")
  processCaptcha=config.getboolean("user","processCaptcha")
  processCaptchaDuplicate=config.getboolean("user","processCaptchaDuplicate")
  useClientInventory=config.getboolean("user","useClientInventory")
  useVariantInventory=config.getboolean("user","useVariantInventory")
  market=config.get("market",marketLocale)
  marketDomain=config.get("marketDomain",marketLocale)
  clientId=config.get("clientId",parametersLocale)
  sitekey=config.get("sitekey",parametersLocale)
  duplicate=config.get("duplicate","duplicate")
  cookies=config.get("cookie","cookie")
  sleeping=config.getint("sleeping","sleeping")

  print(d_()+s_("Market Locale")+lb_(marketLocale))
  print(d_()+s_("Parameters Locale")+lb_(parametersLocale))
  print(d_()+s_("Market")+lb_(market))
  print(d_()+s_("Market Domain")+lb_(marketDomain))
  print(d_()+s_("Market Client ID")+lb_(clientId))
  print(d_()+s_("Market Site Key")+lb_(sitekey))
  print(d_()+s_("Captcha Duplicate")+lb_(duplicate))
  print(d_()+s_("Cookie")+lb_(cookies))
  print(d_()+s_("Process Captcha")+lb_(processCaptcha))
  print(d_()+s_("Use Duplicate")+lb_(processCaptchaDuplicate))
  print(d_()+s_("Product ID")+lb_(masterPid))
  print(d_()+s_("Desired Size")+lb_(mySizes))
  if useVariantInventory:
    print(d_()+s_("Variant Endpoint"))
    response=getVariantResponse(market,marketLocale,marketDomain,parametersLocale,masterPid)
    productJSON=json.loads(response.text)
    productInfo=canonicalizeProductInfoVariant(productJSON)
    printProductInfo(productInfo)
  if useClientInventory:
    print(d_()+s_("Client Endpoint"))
    response=getClientResponse(clientId,marketLocale,parametersLocale,masterPid)
    productJSON=json.loads(response.text)
    productInfo=canonicalizeProductInfoClient(productJSON,masterPid)
    printProductInfo(productInfo)
  processATC=False
  if productInfo["productCount"] > 0:
    processATC=True
  else:
    print (d_()+x_("Variant Count")+lr_("0"))
  if processATC:
    captchaToken=""
    for mySize in mySizes:
      try:
        mySizeATS=productInfo["productStock"][mySize]["ATS"]
        if mySizeATS == 0:
          continue
        print (d_()+s_("Add-To-Cart")+mySize+" : "+str(mySizeATS))
        pid=productInfo["productStock"][mySize]["pid"]
        if processCaptcha:
          captchaToken=getACaptchaToken(apikey2captcha,sitekey,marketDomain,proxy2Captcha,sleeping)
        addToCart(pid,market,marketLocale,marketDomain,processCaptcha,captchaToken,processCaptchaDuplicate,duplicate,cookies,sleeping)
      except:
        print (d_()+x_("Add-To-Cart")+lr_(mySize+" : "+"Not Found"))
