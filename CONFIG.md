# README for config.md

##Section [debug]
`debug` = `True | False` - controls output verbosity. 

`pauseBeforeBrowserQuit` = `True | False` - controls manual interaction before brower quits (before proceeding to the next size). 

##Section [user]
`marketLocale` = `XX` - defines the locale you wish to ATC in.

`parametersLocale` = `US | EU | AU | CA` - defines the region locale for `sitekey` and `clientId`.

`masterPid` = `XX####` - defines the product ID of the item you wish to ATC.

`proxy2Captcha` = `user:password@ip:port | ip:port` - defines the proxy IP that 2Captcha solvers will use to solve the captcha on.

`apikey2captcha` = `xxxxxxxxxxxxxxxxxx` - defines your API key from 2Captcha.com. Do not share your API key!

`processCaptcha` = `True | False` - does a captcha need to be solved?

`processCaptchaDuplicate` = `True | False` - does this product require passing in a captcha duplicate in the ATC payload?

`useClientInventory` = `True | Fase` - use inventory endpoint that requires a valid client ID?

`useVariantInventory` = `True | False` - use inventory endpoint that requires only the product ID?

`mySizes` = `#, #, #, #` - a comma deliminated size list to attempt to cart.

##Section [harvest]
`manuallyHarvestTokens` = `True | False` - Do we want to manually harvest captcha tokens?

`numberOfTokens` = `#` - defines the number of captchas to correctly solve before ATC begins.

`harvestDomain` = `dev.adidas.xxx` - defines the domain we are spoofing to manually harvest captchas.

`phpServerPort` = `####` - defines the PHP server port.

##Section [sleeping]
`sleeping` = `#` - defines the length of time the script will wait between certain time-sensitive events. 

##Section [clientId]
`apiEnv` = `production | staging | development` - defines the API environment of the client inventory endpoint.

`XX` = `xxxxxxxxx` - defines the client ID for locale XX.

##Section [sitekey]
`XX` = `xxxxxxxxx` - defines the captcha sitekey for locale XX.

##Section [duplicate]
`duplicate` = `xxxxx` - defines the duplicate captcha field name.

##Section [cookie]
`cookie` = `cookiename=cookievalue;` - defines a cookie that will be set before each ATC.

##Section [script]
`scriptURL` = `http://xxx.js` - defines a script URL we will inject before each ATC.

##Section [market]
`XX` = `xxxxxxxxx` - defines the market code for locale XX.

##Section [marketDomain]
`XX` = `adidas.xxx` - defines the domain for locale XX.
