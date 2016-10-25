# d3stryr-3stripes
Python 3 implementation of d3stryr-3stripes

# Questions/Problems/Lurking: [http://bit.ly/d3stripesQA](http://bit.ly/d3stripesQA) 

## Requirements:
1. Python 3 (Google how to get it)
   
   Required modules: selenium, requests, virtualenv (optional - but is used in the instructions)
   
   If you don't have virtualenv and want to be able to follow the directions completely then install it with:
   
   ```
   pip3 install virtualenv
   ```

2. chromedriver - [https://sites.google.com/a/chromium.org/chromedriver/](https://sites.google.com/a/chromium.org/chromedriver/)

   Neededed to drive Chrome.
   Download the appropriate version for your OS.

   **Windows** users: place the `chromedriver.exe` file in `C:\Windows` folder.

   **Mac/Linux** users: place the `chromedriver` file in the same folder as `d3stryr-3stripes.py`.

## Installing:

1. Either use git to clone this repository or click on "Download Zip"
2. Navigate to the `d3stryr-3stripes` or `d3stryr-3stripes-master` depending on what you did in step 1. 
   
   I will assume that if you are using `git clone` then you already know how to navigate to the appropriate folder. For everyone else, unzip `d3stryr-3stripes-master.zip`.  Then move the folder into your home directory. Then open up a terminal window and type the following to navigate to the `d3stryr-3stripes-master` folder:
   ```
   cd d3stryr-3stripes-master
   ```

3. Create a virtual environment (only needs to be done once per install):

   ```
   virtualenv -p python3 --no-site-packages .
   ```
   
   Dont forget the period at the end!

4. Activate the virtual environment (needs to be done for once for an active session in your terminal):

   ```
   source bin/activate
   ```
   
5. Install the requirements (needs to be done once per install):

   ```
   pip3 install -r requirements.txt
   ```
   
That is all that is needed to install.

## Configuring:

The only file that needs to be modified is `config.cfg`
```
marketLocal = US
```
Defines the region you are carting. For example `US` (United States), `GB` (United Kingdom), `FR` (France), `CA` (Canada)

```
parametersLocale = US
```
Defines the region for the clientId and sitekey. Possible values: `US`, `EU`, or `AU`

```
masterPid = AQ7403
```
Defines the SKU for the item you wish to cart. The SKU must exist for the region marketLocale you chose.

```
proxy2Captcha = user:password@ip:port
```
Required when processCaptcha is `True`. This defines the proxy 2Captcha will used to solve the captcha on. Yes, you need to provide them with a proxy that they can access. So you either need to provide user:password credentials OR whitelist their IP addresses.

What do I do? Spin up my own VMs in the cloud and run squid3 to setup a temporary proxy with open access. Then tear down the VMs after the drop.

```
apikey2captcha = xXxXxXxXxXxXxXxXxXxXxXxXxXxXx
```
Required when processCaptcha is `True`. This is your 2Captcha API key. [Where to get one](https://2captcha.com/)

```
processCaptcha = False
```
Are we going to solve captcha for the product you are carting? Possible values: `True`, `False`

```
processCaptchaDuplicate = False
```
Do we need to supply a captcha duplicate field name for the product you are carting? Possible values: `True`, `False`
You will likely set this to True for Yeezys. And False for everything else.

```
useClientInventory = True
```
Toggles the use of the client endpoint for inventory. Requires a valid clientId. Possible values: `True`, `False`

```
useVariantInventory = False
```
Toggles the use of the variant endpoint for inventory. Possible values: `True`, `False`

```
mySizes = 5.5, 8.5, 9, M, L
```

A list of sizes you wish to attempt to cart - in the order that they will be attempted. Seperate each value with a comma.

That is it. That is all that needs to be adjusted when clientId and sitekey are working.

If the clientId, sitekey, duplicate, or cookie needs to be adjusted - it will be done in `config.cfg`

## Running
Make sure you have activated the virtual environment:

```
source bin/activate
```

Then run:

```
./d3stryr-3stripes.py
```
## To-Do List
  * Comment parts of the code so that it can be used as a learning tool.
  * Add in the abililty to manually solve captchas if desired.
  * Adjust terminal coloring for Windows.
  * Interface w/ a MySQL DB for token harvesting locally.

## Not-Gonna-Do List
  * Auto-checkout. I much prefer 10,000 people getting a pair versus 1,000 people getting 10 pairs.

## Common Problems
  * If the command `pip3 install virtualenv` does not work then you will need to install pip3. More than likely the command will be:
    
    ```
    easy_install pip3
    ```
    
    or 
    
    ```
    easy_install pip
    ```
    If that doesnt work then Google "how to install pip3 python3" for your OS.
  * If you get a browser window with "data;" as the URL then you will need to download the latest chromedriver version for your OS.  See the instructions at the top of this README.
