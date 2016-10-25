from random import randint

def agent():
  """Returns a random user-agent."""
  browsers=[
      "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4",
      "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4",
      "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
      "Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",
      "Mozilla/5.0 (iPad; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5",
      "Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true",
      "Mozilla/5.0 (Linux; U; en-us; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us; Silk/1.0.141.16-Gen4_11004310) AppleWebkit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true",
      "Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; Nexus S Build/GRJ22) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
      "Mozilla/5.0 (Linux; Android 4.3; Nexus 7 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.72 Safari/537.36",
      "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
      "Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+",
      "Mozilla/5.0 (Linux; Android 4.3; Nexus 10 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.72 Safari/537.36",
      "Mozilla/5.0 (Linux; U; Android 2.3; en-us; SAMSUNG-SGH-I717 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
      "Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
      "Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
      "Mozilla/5.0 (Linux; Android 4.2.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; U; Android 2.2; en-us; SCH-I800 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
  ]
  string = browsers[randint(0,len(browsers)-1)]
  return string

class color:
  reset='\033[0m'
  bold='\033[01m'
  disable='\033[02m'
  underline='\033[04m'
  reverse='\033[07m'
  strikethrough='\033[09m'
  invisible='\033[08m'
  black='\033[30m'
  red='\033[31m'
  green='\033[32m'
  orange='\033[33m'
  blue='\033[34m'
  purple='\033[35m'
  cyan='\033[36m'
  lightgrey='\033[37m'
  darkgrey='\033[90m'
  lightred='\033[91m'
  lightgreen='\033[92m'
  yellow='\033[93m'
  lightblue='\033[94m'
  pink='\033[95m'
  lightcyan='\033[96m'

import datetime

def d_(destroyerId=None):
  if destroyerId is not None:
    return "Destroyer # "+str(destroyerId).rjust(4," ")+" "+str(datetime.datetime.now().time().strftime("%I:%M:%S.%f")[:-3])
  else:
    return "Destroyer # BASE "+str(datetime.datetime.now().time().strftime("%I:%M:%S.%f")[:-3])
def s_(string):
  return color.lightgrey+" ["+str(string).center(20," ")+"]"+color.reset+" "
def x_(string):
  return color.lightred+" ["+str(string).center(20," ")+"]"+color.reset+" "
def lb_(string):
  return color.lightblue+str(string)+color.reset
def lr_(string):
  return color.lightred+str(string)+color.reset
def y_(string):
  return color.yellow+str(string)+color.reset

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def launchChrome(session,baseADCUrl,cartURL,sleeping):
  if "nt" in  os.name:
    chromedriver = "C:\Windows\chromedriver.exe"
  else:
    chromedriver = "./chromedriver"
  os.environ["webdriver.chrome.driver"] = chromedriver
  browser = webdriver.Chrome(chromedriver)
  browser.get(baseADCUrl)
  for key, val in session.cookies.iteritems():
    browser.add_cookie({'name':key,'value':val})
  time.sleep(sleeping)
  browser.get(cartURL)
  temp=input("Press Enter to Continue")
  browser.quit()
  return

import configparser
import json
import requests

requests.packages.urllib3.disable_warnings()

def getACaptchaToken(apikey2captcha,sitekey,marketDomain,proxy2Captcha,sleeping):
  session=requests.Session()
  session.verify=False
  session.cookies.clear()
  pageurl="http://www."+marketDomain
  print (d_()+s_("pageurl")+lb_(pageurl))
  while True:
    data={
     "key":apikey2captcha,
     "action":"getbalance",
     "json":1,
    }
    response=session.get(url="http://2captcha.com/res.php",params=data)
    JSON=json.loads(response.text)
    if JSON["status"] == 1:
      balance=JSON["request"]
      print (d_()+s_("Balance")+lb_("$"+str(balance)))
    else:
      print (d_()+x_("Balance"))
    CAPTCHAID=None
    proceed=False
    while not proceed:
      data={
       "key":apikey2captcha,
       "method":"userrecaptcha",
       "googlekey":sitekey,
       "proxy":proxy2Captcha,
       "proxytype":"HTTP",
       "pageurl":pageurl,
       "json":1
      }
      response=session.post(url="http://2captcha.com/in.php",data=data)
      JSON=json.loads(response.text)
      if JSON["status"] == 1:
        CAPTCHAID=JSON["request"]
        proceed=True
        print (d_()+s_("Captcha ID")+lb_(CAPTCHAID))
      else:
        print (d_()+x_("Response")+y_(response.text))
        print (d_()+x_("Sleeping")+y_(str(sleeping)+" seconds"))
        time.sleep(sleeping)
    print (d_()+s_("Waiting")+str(sleeping)+" seconds before polling for Captcha response")
    time.sleep(sleeping)
    TOKEN=None
    proceed=False
    while not proceed:
      data={
       "key":apikey2captcha,
       "action":"get",
       "json":1,
       "id":CAPTCHAID,
      }
      response=session.get(url="http://2captcha.com/res.php",params=data)
      JSON=json.loads(response.text)
      if JSON["status"] == 1:
        TOKEN=JSON["request"]
        proceed=True
        print (d_()+s_("Token ID")+lb_(TOKEN))
      else:
        print (d_()+x_("Response")+y_(response.text))
        print (d_()+x_("Sleeping")+y_(str(sleeping)+" seconds"))
        time.sleep(sleeping)
    data={
     "key":apikey2captcha,
     "action":"getbalance",
     "json":1,
    }
    response=session.get(url="http://2captcha.com/res.php",params=data)
    JSON=json.loads(response.text)
    if JSON["status"] == 1:
      balance=JSON["request"]
      print (d_()+s_("Balance")+lb_("$"+str(balance)))
    else:
      print (d_()+x_("Balance"))
    if TOKEN is not None:
      return TOKEN

def getClientResponse(clientId,marketLocale,parametersLocale,masterPid):
  headers = {
    'User-Agent':agent(),
  }
  session=requests.Session()
  session.verify=False
  session.cookies.clear()
  skus=masterPid+","
  for x in range(510,820,10):
    skus=skus+masterPid+"_"+str(x)+",";
  #Other countries will use US format like MX. They can just request US value for parametersLocale in config.cfg
  if parametersLocale == "US":
    clientStockURL="http://production-us-adidasgroup.demandware.net/s/adidas-"+marketLocale+"/dw/shop/v16_5/products/("+skus+")?client_id="+clientId+"&expand=availability,variations,prices"
  else:
    clientStockURL="http://production-store-adidasgroup.demandware.net/s/adidas-"+marketLocale+"/dw/shop/v16_5/products/("+skus+")?client_id="+clientId+"&expand=availability,variations,prices"
  response=session.get(url=clientStockURL,headers=headers)
  return response

def getVariantResponse(market,marketLocale,marketDomain,parametersLocale,masterPid):
  headers = {
    'User-Agent':agent(),
  }
  session=requests.Session()
  session.verify=False
  session.cookies.clear()
  #Not sure why I even bother making a case for Portugal if dude on twitter keeps telling it doesnt work. Da fuq is MLT?
  if market == "PT":
    variantStockURL="http://www."+marketDomain+"/on/demandware.store/Sites-adidas-"+marketLocale+"-Site/"+"MLT"+"/Product-GetVariants?pid="+masterPid
  else:
    variantStockURL="http://www."+marketDomain+"/on/demandware.store/Sites-adidas-"+marketLocale+"-Site/"+market+"/Product-GetVariants?pid="+masterPid
  response=session.get(url=variantStockURL,headers=headers)
  return response

def canonicalizeProductInfoClient(productJSON,masterPid):
  #Initialize a dictionary.
  productInfo={}
  productInfo["productStock"]={}
  #Because of how we order the skus in clientStockURL 0-index is always masterPid info in the JSON response.
  data = productJSON["data"][0]
  try:
    productInfo["productName"]=data["name"]
  except:
    productInfo["productName"]="/"
  try:
    productInfo["productColor"]=data["c_defaultColor"]
  except:
    productInfo["productColor"]="/"
  try:
    productInfo["productOrderable"]=data["inventory"]["orderable"]
  except:
    productInfo["productOrderable"]=False
  try:
    productInfo["productPrice"]=data["price"]
  except:
    productInfo["productPrice"]=0
  try:
    productInfo["productCount"]=productJSON["count"]-1
  except:
    productInfo["productCount"]=0
  try:
    productInfo["productATS"]=data["inventory"]["ats"]
  except:
    productInfo["productATS"]=0
  try:
    productInfo["productStockLevel"]=data["inventory"]["stock_level"]
  except:
    productInfo["productStockLevel"]=0
  """
  Because data[""c_sizeFTW"] and data["c_sizeSearchValue"] yield nonsense for some EU locales:
  Build a dictionary to convert adidas _XXX sizing to canonical sizing.
  """
  adidasSize2Size={}
  for variant in data["variation_attributes"][0]["values"]:
    adidasSize2Size[masterPid+"_"+variant["value"]]=variant["name"]
  """
  We could avoid:
    if data["id"] != masterPid:
  by using a for loop to iterate through:
    range(1,len(productJSON["data"])):
  But I doubt there is a performance hit here. Because this is only done once even if threading is introducde in the future.
  """
  for data in productJSON["data"]:
    if data["id"] != masterPid:
      try:
        productInfo["productStock"][adidasSize2Size[data["id"]]]={}
        productInfo["productStock"][adidasSize2Size[data["id"]]]["ATS"]=int(data["inventory"]["ats"])
        productInfo["productStock"][adidasSize2Size[data["id"]]]["pid"]=data["id"]
      except:
        print(d_()+x_("Client Inventory"))
  return productInfo

def canonicalizeProductInfoVariant(productJSON):
  productInfo={}
  productInfo["productStock"]={}
  productInfo["productName"]="/"
  productInfo["productColor"]="/"
  productInfo["productOrderable"]="/"
  try:
    productInfo["productPrice"]=productJSON["variations"]["variants"][0]["pricing"]["standard"]
  except:
    productInfo["productPrice"]=0
  try:
    productInfo["productCount"]=len(productJSON["variations"]["variants"])
  except:
    productInfo["productCount"]=0
  productInfo["productATS"]=0
  try:
    for variant in productJSON["variations"]["variants"]:
      productInfo["productATS"]=productInfo["productATS"]+int(variant["ATS"])
      productInfo["productStock"][variant["attributes"]["size"]]={}
      productInfo["productStock"][variant["attributes"]["size"]]["ATS"]=int(variant["ATS"])
      productInfo["productStock"][variant["attributes"]["size"]]["pid"]=variant["id"]
  except:
    print(d_()+x_("Variant Inventory"))
  productInfo["productStockLevel"]=productInfo["productATS"]
  return productInfo

def printProductInfo(productInfo):
  print(d_()+s_("Product Name")+lb_(productInfo["productName"]))
  print(d_()+s_("Product Color")+lb_(productInfo["productColor"]))
  print(d_()+s_("Price")+lb_(productInfo["productPrice"]))
  print(d_()+s_("Orderable")+lb_(productInfo["productOrderable"]))
  print(d_()+s_("ATS")+lb_(str(productInfo["productATS"]).rjust(6," ")))
  print(d_()+s_("Stock Level")+lb_(str(productInfo["productStockLevel"]).rjust(6," ")))
  print(d_()+s_("Size Inventory"))
  for size in sorted(productInfo["productStock"]):
    print(d_()+s_(size.ljust(5," ")+" / "+productInfo["productStock"][size]["pid"])+lb_(str(productInfo["productStock"][size]["ATS"]).rjust(6," ")))
  return

def addToCart(pid,market,marketLocale,marketDomain,processCaptcha,captchaToken,processCaptchaDuplicate,duplicate,cookies,sleeping):
  atcSession=requests.Session()
  atcSession.verify=False
  atcSession.cookies.clear()
  if marketLocale == "PT":
    baseADCUrl="http://www."+marketDomain+"/on/demandware.store/Sites-adidas-"+"MLT"+"-Site/"+market
  else:
    baseADCUrl="http://www."+marketDomain+"/on/demandware.store/Sites-adidas-"+marketLocale+"-Site/"+market
  atcURL=baseADCUrl+"/Cart-MiniAddProduct"
  cartURL=baseADCUrl.replace("http://","https://")+"/Cart-Show"
  """
  We do a request to a searchURL for the masterPid in hopes of establishing cookies for a session.
  This does not seem to help reduce the occurrences of soft ban on stalled Cart-Shows after multiple page refreshes.
  """
  searchURL=baseADCUrl.replace("http://","https://")+"/Search-GetSuggestions?isSuggestions=true&isCategories=false&isProducts=true&q="+pid.split("_")[0]
  headers = {
    'User-Agent':agent(),
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer':"http://www."+marketDomain+"/",
  }
  response=atcSession.get(url=searchURL,headers=headers)
  headers = {
    'User-Agent':agent(),
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Referer':"http://www."+marketDomain+"/",
  }
  data={}
  #If we are processing captcha then add to our payload.
  if processCaptcha:
    data["g-recaptcha-response"]=captchaToken
  #If we need captcha duplicate then add to our payload.
  if processCaptchaDuplicate:
    #If cookies need to be set then add to our payload.
    if "neverywhere" not in cookies:
      headers["Cookie"]=cookies
    #Alter the atcURL for the captcha duplicate case
    atcURL=atcURL+"?clientId="+clientId
    #Add captcha duplicate  to our payload.
    data[duplicate]=captchaToken
  data["pid"]=pid
  data["Quantity"]="1"
  data["request"]="ajax"
  data["responseformat"]="json"
  response=atcSession.post(url=atcURL,data=data,headers=headers)
  #Im told I could just do atcJSON=resposne.json but I'm a creature of habit.
  #If threaded then you'll want to revisit and adjust.
  atcJSON=json.loads(response.text)
  print (d_()+s_("JSON")+"\n"+y_(json.dumps(atcJSON,indent=2)))
  try:
    if atcJSON["result"]=="SUCCESS":
      print(d_()+s_("Success")+lb_(atcJSON["basket"][-1]["product_id"]+" : " +str(atcJSON["basket"][-1]["quantity"])+" x "+str(atcJSON["basket"][-1]["price"])))
      #We pass the request session to launchChrome so we can upload cookies to Chrome (transfering a session to the browser).
      launchChrome(atcSession,baseADCUrl,cartURL,sleeping)
    else:
      print (d_()+x_("JSON")+"\n"+lr_(json.dumps(atcJSON,indent=2)))
  except:
    if "Access Denied" in response.text:
      print (d_()+x_("ATC JSON RESULTS")+lr_("Access Denied"))
    else:
      print (d_()+x_("ATC JSON RESULTS")+lr_("Unable to parse response")+"\n"+y_(response.text))
