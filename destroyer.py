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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def launchChrome(session,cartURL):
  chrome_options = Options()
  browser = webdriver.Chrome(chrome_options=chrome_options)
  browser.get(cartURL)
  for key, val in session.cookies.iteritems():
    browser.add_cookie({'name':key,'value':val})
  browser.refresh()
  temp=input("Press Enter to Continue")
  browser.quit()
  return

import configparser
import json
import requests
import time

def getACaptchaToken(apikey2captcha,sitekey,pageURL,proxy2Captcha):
  config = configparser.ConfigParser()
  configFilePath = "config.cfg"
  config.read(configFilePath)

  sleeping=config.getint("sleeping","sleeping")

  captchaSession=requests.Session()
  captchaSession.cookies.clear()
  captchaSession.verify=False
  while True:
    data={
     "key":apikey2captcha,
     "action":"getbalance",
     "json":1,
    }
    response=captchaSession.get(url="http://2captcha.com/res.php",params=data)
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
       "pageurl":pageURL,
       "json":1
      }
      response=captchaSession.post(url="http://2captcha.com/in.php",data=data)
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
      response=captchaSession.get(url="http://2captcha.com/res.php",params=data)
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
    response=captchaSession.get(url="http://2captcha.com/res.php",params=data)
    JSON=json.loads(response.text)
    if JSON["status"] == 1:
      balance=JSON["request"]
      print (d_()+s_("Balance")+lb_("$"+str(balance)))
    else:
      print (d_()+x_("Balance"))
    if TOKEN is not None:
      return TOKEN
