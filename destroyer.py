import configparser
#Parse configuration file
config = configparser.ConfigParser()
configFilePath = "config.cfg"
config.read(configFilePath)
#Get the size array
mySizes=config.get("user","mySizes").split(",")
#Strip leading and trailing whitespaces if present in each array index and store back into mySizes array
mySizes = [size.strip() for size in mySizes]
#Pull user info for locale
marketLocale=config.get("user","marketLocale")
parametersLocale=config.get("user","parametersLocale")
#Pull user info for masterPid
masterPid=config.get("user","masterPid")
#Token Harvesting info
manuallyHarvestTokens=config.getboolean("harvest","manuallyHarvestTokens")
numberOfTokens=config.getint("harvest","numberOfTokens")
phpServerPort=config.get("harvest","phpServerPort")
harvestDomain=config.get("harvest","harvestDomain")
captchaTokens=[]
#Pull 2captcha info
proxy2Captcha=config.get("user","proxy2Captcha")
apikey2captcha=config.get("user","apikey2captcha")
#Pull run parameters for handing inventory endpoints
useClientInventory=config.getboolean("user","useClientInventory")
useVariantInventory=config.getboolean("user","useVariantInventory")
#Pull run parameters for handing captchas
processCaptcha=config.getboolean("user","processCaptcha")
processCaptchaDuplicate=config.getboolean("user","processCaptchaDuplicate")
#Pull info based on marketLocale
market=config.get("market",marketLocale)
marketDomain=config.get("marketDomain",marketLocale)
#Pull info based on parametersLocel
apiEnv=config.get("clientId","apiEnv")
clientId=config.get("clientId",parametersLocale)
sitekey=config.get("sitekey",parametersLocale)
#Pull info necessary for a Yeezy drop
duplicate=config.get("duplicate","duplicate")
cookies=config.get("cookie","cookie")
#Pull the amount of time to sleep in seconds when needed
sleeping=config.getint("sleeping","sleeping")
#Are we debugging?
debug=config.getboolean("debug","debug")

#We will use os to acquire details of the operating system so we can determine if we are on Windows or not.
import os

if "nt" in  os.name:
#We remove ANSI coloring for Windows
  class color:
    reset=''
    bold=''
    disable=''
    underline=''
    reverse=''
    strikethrough=''
    invisible=''
    black=''
    red=''
    green=''
    orange=''
    blue=''
    purple=''
    cyan=''
    lightgrey=''
    darkgrey=''
    lightred=''
    lightgreen=''
    yellow=''
    lightblue=''
    pink=''
    lightcyan=''
else:
#We use ANSI coloring for OSX/Linux
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

#We use datetime to acquire the date and time
import datetime

#In a threaded setup you can identify a printed line by its threadId - I just call it destroyerId
def d_(destroyerId=None):
  if destroyerId is not None:
    return "Destroyer # "+str(destroyerId).rjust(4," ")+" "+str(datetime.datetime.now().time().strftime("%I:%M:%S.%f")[:-3])
  else:
    return "Destroyer # BASE "+str(datetime.datetime.now().time().strftime("%I:%M:%S.%f")[:-3])
def s_(string):
  return color.lightgrey+" ["+str(string).center(21," ")+"]"+color.reset+" "
#Color for exceptions
def x_(string):
  return color.lightred+" ["+str(string).center(21," ")+"]"+color.reset+" "
#Color for debugging
def z_(string):
  return color.orange+" ["+str(string).center(21," ")+"]"+color.reset+" "
#Colorize text with lightblue
def lb_(string):
  return color.lightblue+str(string)+color.reset
#Colorize text with lightred
def lr_(string):
  return color.lightred+str(string)+color.reset
#Colorize text with yellow
def y_(string):
  return color.yellow+str(string)+color.reset
#Colorize text with orange
def o_(string):
  return color.orange+str(string)+color.reset

def printRunParameters():
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
  print(d_()+s_("Manual Token Harvest")+lb_(manuallyHarvestTokens))
  print(d_()+s_("Tokens to Harvest")+lb_(numberOfTokens))
  if debug:
    print(d_()+z_("Sleeping")+o_(sleeping))
    print(d_()+z_("Debug")+o_(debug))
  return

#randint allows us to obtain an random integer between two integer values a and b: int=randint(a,b)
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
  #In this usage we acquire a random index of the browser array.
  string = browsers[randint(0,len(browsers)-1)]
  return string

#We use time to sleep
import time
#We use selenium for browser automation
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def launchChrome(session,baseADCUrl,cartURL,sleeping):
  if "nt" in  os.name:
  #Es ventanas?
    chromedriver = "C:\Windows\chromedriver.exe"
  else:
  #Es manzanas?
    chromedriver = "./chromedriver"
  os.environ["webdriver.chrome.driver"] = chromedriver
  chrome_options = Options()
  #We store the browsing session in ChromeFolder so we can manually delete it if necessary
  chrome_options.add_argument("--user-data-dir=ChromeFolder")
  browser = webdriver.Chrome(chromedriver,chrome_options=chrome_options)
  browser.get(baseADCUrl)
  #Push cookies from request to Google Chrome
  for key, val in session.cookies.iteritems():
    if debug:
      print(d_()+z_("Debug:Key")+o_(key))
      print(d_()+z_("Debug:Val")+o_(val))
    browser.add_cookie({'name':key,'value':val})
  time.sleep(sleeping)
  browser.get(baseADCUrl+"/Cart-ProductCount")
  browser.get(cartURL.replace("/Cart-Show","/CODelivery-Start"))
  temp=input("Press Enter to Continue")
  browser.quit()
  return

import configparser
import json
import requests

requests.packages.urllib3.disable_warnings()

def getACaptchaToken():
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
        XCAPTCHAID="🐨 🐢 🐨 🐢 🐨 🐢 🐨 🐢 🐨 🐢"
        proceed=True
        print (d_()+s_("Captcha ID")+lb_(XCAPTCHAID))
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

def getClientResponse():
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
    clientStockURL="http://"+apiEnv+"-us-adidasgroup.demandware.net/s/adidas-"+marketLocale+"/dw/shop/v15_6/products/("+skus+")?client_id="+clientId+"&expand=availability,variations,prices"
  else:
    clientStockURL="http://"+apiEnv+"-store-adidasgroup.demandware.net/s/adidas-"+marketLocale+"/dw/shop/v15_6/products/("+skus+")?client_id="+clientId+"&expand=availability,variations,prices"
  if debug:
    print(d_()+z_("Debug")+o_(clientStockURL))
  response=session.get(url=clientStockURL,headers=headers)
  return response

def getVariantResponse():
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
  if debug:
    print(d_()+z_("Debug")+o_(variantStockURL))
  response=session.get(url=variantStockURL,headers=headers)
  return response

def canonicalizeProductInfoClient(productJSON):
  #Initialize a dictionary.
  productInfo={}
  productInfo["productStock"]={}
  #Because of how we order the skus in clientStockURL 0-index is always masterPid info in the JSON response.
  try:
    data = productJSON["data"][0]
  except:
    print(d_()+x_("Parse Client JSON"))
    return productInfo
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
  if debug:
    print(d_()+z_("Debug")+o_(json.dumps(productInfo,indent=2)))
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
  if debug:
    print(d_()+z_("Debug")+o_(json.dumps(productInfo,indent=2)))
  return productInfo

def getProductInfo():
  if useClientInventory:
    try:
      print(d_()+s_("Client Endpoint"))
      response=getClientResponse()
      productJSON=json.loads(response.text)
      productInfoClient=canonicalizeProductInfoClient(productJSON)
      return productInfoClient
    except:
      print(d_()+x_("Client Endpoint"))
      if debug:
        print(d_()+z_("Debug")+o_("Client Endpoint Response -"+response.text))
  #If we reached this point then useClientInventory didn't successfully return.
  #So lets proceed with useVariantInventory.
  try:
    print(d_()+s_("Variant Endpoint"))
    response=getVariantResponse()
    productJSON=json.loads(response.text)
    productInfoVariant=canonicalizeProductInfoVariant(productJSON)
    return productInfoVariant
  except:
    print(d_()+x_("Variant Endpoint"))
    if debug:
      print(d_()+z_("Debug")+o_("Variant Endpoint Response -"+response.text))
  #If we reached this point then useVariantInventory did not successfully reutrn.
  #So lets produce at minimum size inventory.
  #We will refer to this as Fallback for productInfo (when both client and variant produces no inventory result).
  productInfoFallback={}
  productInfoFallback["productStock"]={}
  productInfoFallback["productName"]="/"
  productInfoFallback["productColor"]="/"
  productInfoFallback["productOrderable"]="/"
  productInfoFallback["productPrice"]=0
  productInfoFallback["productCount"]=-1
  productInfoFallback["productATS"]=-1
  productInfoFallback["productStockLevel"]=-1
  #US vs EU sizing seems to be off by 0.5 size
  if parametersLocale == "US":
    literalSize=4.5
    for variant in range(540, 750, 10):
      stringLiteralSize=str(literalSize).replace(".0","")
      productInfoFallback["productStock"][stringLiteralSize]={}
      productInfoFallback["productStock"][stringLiteralSize]["ATS"]=1
      productInfoFallback["productStock"][stringLiteralSize]["pid"]=masterPid+"_"+str(variant)
      literalSize=literalSize+.5
  else:
    literalSize=4.5
    for variant in range(550, 750, 10):
      stringLiteralSize=str(literalSize).replace(".0","")
      productInfoFallback["productStock"][stringLiteralSize]={}
      productInfoFallback["productStock"][stringLiteralSize]["ATS"]=1
      productInfoFallback["productStock"][stringLiteralSize]["pid"]=masterPid+"_"+str(variant)
      literalSize=literalSize+.5
  return productInfoFallback

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

from collections import deque

def processAddToCart(productInfo):
  captchaTokensReversed=[]
  if manuallyHarvestTokens:
    harvestTokensManually()
    for index in range(0,len(captchaTokens)):
      captchaTokensReversed.append(captchaTokens.pop())

  for mySize in mySizes:
    try:
      mySizeATS=productInfo["productStock"][mySize]["ATS"]
      if mySizeATS == 0:
        continue
      print (d_()+s_("Add-To-Cart")+mySize+" : "+str(mySizeATS))
      pid=productInfo["productStock"][mySize]["pid"]
      #Check if we need to process captcha
      captchaToken=""
      if processCaptcha:
        #See if we have any manual tokens available
        if len(captchaTokensReversed) > 0:
          #Use a manual token
          captchaToken=captchaTokensReversed.pop()
          print (d_()+s_("Number of Tokens Left")+lb_(len(captchaTokensReversed)))
        else:
          #No manual tokens to pop - so lets use 2captcha
          captchaToken=getACaptchaToken()
      addToCartChromeAJAX(pid,captchaToken)
#     addToCartRequestTransferToChrome(pid,captchaToken)
    except:
      print (d_()+x_("Add-To-Cart")+lr_(mySize+" : "+"Not Found"))

def addToCartRequestTransferToChrome(pid,captchaToken):
  atcSession=requests.Session()
  atcSession.verify=False
  atcSession.cookies.clear()
  if marketLocale == "PT":
    baseADCUrl="http://www."+marketDomain+"/on/demandware.store/Sites-adidas-"+"MLT"+"-Site/"+market
  else:
    baseADCUrl="http://www."+marketDomain+"/on/demandware.store/Sites-adidas-"+marketLocale+"-Site/"+market
  atcURL=baseADCUrl+"/Cart-MiniAddProduct"
  cartURL=baseADCUrl.replace("http://","https://")+"/Cart-Show"
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
  if debug:
    print(d_()+z_("Debug")+o_(json.dumps(data,indent=2)))
    print(d_()+z_("Debug")+o_(atcURL))
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

def addToCartChromeAJAX(pid,captchaToken):
  if marketLocale == "PT":
    baseADCUrl="http://www."+marketDomain+"/on/demandware.store/Sites-adidas-"+"MLT"+"-Site/"+market
  else:
    baseADCUrl="http://www."+marketDomain+"/on/demandware.store/Sites-adidas-"+marketLocale+"-Site/"+market
  atcURL=baseADCUrl+"/Cart-MiniAddProduct"
  cartURL=baseADCUrl.replace("http://","https://")+"/Cart-Show"
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
  data["masterPid"]=masterPid
  data["pid"]=pid
  data["Quantity"]="1"
  data["request"]="ajax"
  data["responseformat"]="json"
  script="""
  $.ajax({
    url: '"""+atcURL+"""',
    data: """+json.dumps(data,indent=2)+""",
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
  });
  """
  if debug:
    print(d_()+z_("Debug")+o_(json.dumps(data,indent=2)))
    print(d_()+z_("Debug")+o_(atcURL))
    print(d_()+z_("Debug")+o_(script))
  if "nt" in  os.name:
  #Es ventanas?
    chromedriver = "C:\Windows\chromedriver.exe"
  else:
  #Es manzanas?
    chromedriver = "./chromedriver"
  os.environ["webdriver.chrome.driver"] = chromedriver
  chrome_options = Options()
  #We store the browsing session in ChromeFolder so we can manually delete it if necessary
  chrome_options.add_argument("--user-data-dir=ChromeFolder")
  browser = webdriver.Chrome(chromedriver,chrome_options=chrome_options)
  browser.delete_all_cookies()
  browser.get(baseADCUrl)
  results=browser.execute_script(script)
  time.sleep(sleeping)
  browser.get(baseADCUrl+"/Cart-ProductCount")
  productCount=browser.find_element_by_tag_name('body').text
  productCount=productCount.replace('"',"")
  productCount=productCount.strip()
  if debug:
    print(d_()+z_("Debug")+o_("Product Count"+" : "+productCount))
  if (len(productCount) == 1) and (int(productCount) > 0):
    results=browser.execute_script("window.location='"+cartURL+"'")
    temp=input("Press Enter to Close the Browser & Continue")
  else:
    print (d_()+x_("Product Count")+lr_(productCount))
  #Need to delete all the cookes for this session or else we will have the previous size in cart
  browser.delete_all_cookies()
  browser.quit()
  return

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

def activateCaptcha(driver):
  #Activate the catpcha widget
  iframe=driver.find_element_by_css_selector('iframe[src*="api2/anchor"]')
  driver.switch_to_frame(iframe)
  try:
    CheckBox=WebDriverWait(driver, sleeping).until(expected_conditions.presence_of_element_located((By.ID ,"recaptcha-anchor")))
  except:
    try:
      CheckBox=WebDriverWait(driver, sleeping).until(expected_conditions.presence_of_element_located((By.ID ,"recaptcha-anchor")))
    except:
      print (d_()+x_("Activate Captcha")+lr_("Failed to find checkbox"))
  CheckBox.click()

def checkSolution(driver,mainWindow):
  #Check to see if we solved the captcha
  solved=False
  while not solved:
    driver.switch_to.window(mainWindow)
    try:
      iframe=driver.find_element_by_css_selector('iframe[src*="api2/anchor"]')
    except:
      print (d_()+x_("Check Solution")+lr_("Failed to find checkbox"))
      return
    driver.switch_to_frame(iframe)
    try:
      temp=driver.find_element_by_xpath('//span[@aria-checked="true"]')
      print (d_()+s_("Check Solution")+lb_("Solved"))
      solved=True
    except:
      solved=False
    time.sleep(1)
  return solved

def getToken(driver,mainWindow):
  #We parse the token from the page
  token=None
  driver.switch_to.window(mainWindow)
  try:
    Submit=WebDriverWait(driver, sleeping).until(expected_conditions.presence_of_element_located((By.ID ,"submit")))
    Submit.click()
    time.sleep(1)
  except:
    print (d_()+x_("Captcha Submit")+lr_("Failed to click submit"))
  tokenElement=driver.find_element_by_css_selector('p#token')
  token=tokenElement.get_attribute("value")
  if token is not None:
    print (d_()+s_("Get Token")+lb_(token))
  return token

def harvestTokensManually():
  print (d_()+s_("Manual Token Harvest")+lb_("Number of tokens harvested: "+str(len(captchaTokens))))
  #We will create the harvest.php on the fly based on locale and sitekey values in config.cfg
  htmlSource="""
    <?php
     $siteKey = '"""+sitekey+"""';
     $lang = 'en';
    ?>
     <?php if (isset($_POST['g-recaptcha-response'])): ?>
    <html>
     <head>
       <title>adidas Official Website | adidas</title>
     </head>
     <body>
     <?php $token=$_POST['g-recaptcha-response']; ?>
         <p id="token" value="<?php echo $token; ?>" style="padding: 3px; word-break: break-all; word-wrap: break-word;"><?php echo $token; ?></p>
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
                <div class="g-recaptcha" data-sitekey="<?php echo $siteKey; ?>"></div>
                <script type="text/javascript" src="https://www.google.com/recaptcha/api.js">
                </script>
                <p><input type="submit" value="Submit" id="submit"/></p>
            </fieldset>
        </form>
     <?php endif; ?>
     </body>
    </html>"""
  with open("harvest.php","w") as htmlFile:
    htmlFile.write(htmlSource)
  if "nt" in  os.name:
  #Es ventanas?
    chromedriver = "C:\Windows\chromedriver.exe"
  else:
  #Es manzanas?
    chromedriver = "./chromedriver"
  os.environ["webdriver.chrome.driver"] = chromedriver
  chrome_options = Options()
  windowSize=[
    #browser
    "640,640",
  ]
  #Custom window size.
  chrome_options.add_argument("window-size="+windowSize[0])
  #We store the browsing session in ChromeFolder so we can manually delete it if necessary
  chrome_options.add_argument("--user-data-dir=ChromeFolder")
  browser = webdriver.Chrome(chromedriver,chrome_options=chrome_options)
  browser.delete_all_cookies()
  url="http://"+harvestDomain+":"+phpServerPort+"/harvest.php"
  while len(captchaTokens) < numberOfTokens:
    browser.get(url)
    mainWindow = browser.current_window_handle
    try:
      activateCaptcha(driver=browser)
    except:
      print (d_()+x_("Page Load Failed")+lr_("Did you launch the PHP server?"))
      print (d_()+x_("Page Load Failed")+lr_("Falling back to 2captcha"))
      browser.delete_all_cookies()
      browser.quit()
      return
    solved=checkSolution(driver=browser,mainWindow=mainWindow)
    token=getToken(driver=browser,mainWindow=mainWindow)
    if token is not None:
      if len(captchaTokens) == 0:
        startTime = time.time()
      captchaTokens.append(token)
      print (d_()+s_("Token Added"))
      print (d_()+s_("Manual Token Harvest")+lb_("Number of tokens harvested: "+str(len(captchaTokens))))
    currentTime = time.time()
    elapsedTime = currentTime - startTime
    print (d_()+s_("Total Time Elapsed")+lb_(str(round(elapsedTime,2)) + " seconds"))
  browser.delete_all_cookies()
  browser.quit()
