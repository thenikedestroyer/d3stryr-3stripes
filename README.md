# d3stryr-3stripes
Python 3 implementation of d3stryr-3stripes

# Questions/Problems/Lurking: [http://bit.ly/d3stripesQA](http://bit.ly/d3stripesQA) 

## Requirements:
1. Python 3.5.2 - [https://www.python.org/downloads/](https://www.python.org/downloads/)
   
   Required modules: selenium, requests, virtualenv (optional - but is used in the instructions)
   
   If you don't have virtualenv and want to be able to follow the directions completely then install it with:
   
   ```
   pip3 install virtualenv
   ```
   
   If you don't have pip3 already installed then install it with (assuming you have Python 3.5.x installed):
   
   ```
   easy_install-3.5 pip
   ```
   

2. chromedriver - [https://sites.google.com/a/chromium.org/chromedriver/](https://sites.google.com/a/chromium.org/chromedriver/)

   Neededed to drive Chrome.
   Download the appropriate version for your OS.

   **Windows** users: place the `chromedriver.exe` file in the same folder as `d3stryr-3stripes.py` OR in `C:\Windows` folder.

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
   
   Mac/Linux:
   ```
   source bin/activate
   ```
   Windows:
   ```
   Scripts\activate
   ```
   
5. Install the requirements (needs to be done once per install):

   ```
   pip3 install -r requirements.txt
   ```
   
That is all that is needed to install.

## Configuring:

The only file that needs to be modified is `config.cfg`. Read [CONFIG.md](https://github.com/thenikedestroyer/d3stryr-3stripes/blob/master/CONFIG.md)

## Running
If you are starting from a new terminal and the `d3stryr-3stripes-master` folder is in your home directory then navigate (change into) the `d3stryr-3stripes-master` folder:

```
cd d3stryr-3stripes-master
```

Make sure you have activated the virtual environment:

Mac/Linux:
```
source bin/activate
```
Windows:
```
Scripts\activate
```

Then you are ready to run:

Mac/Linux:
```
./d3stryr-3stripes.py
```
Windows:
```
.\d3stryr-3stripes.py
```

## Program Flow
*  The script will look up the either the Variant endpoint for inventory or the Client endpoint for inventory (or it may do both - with Client stock being used for the remainder of the run).
*  The script will cycle through your size list and check to see if inventory value is greater than 0.
*  If inventory is available it will attempt to cart that size.
*  If `processCaptcha = True` then the script will attempt to get a captcha token.
*  The script then builds the payload for the necessary add-to-cart request.
*  If the response is successful then the script will open up a Chrome browser and attempt to transfer the session over.
*  Chrome will try to access the main locale page first. Then waits several seconds and then navigates to the Cart-Show page.
*  If you get an empty Cart-Show page but the basket in the upper-right has a "1" showing then refresh the page once using (CTRL-R or CMD+R)
*  If nothing appears then quit the browser and move on to the next pair because any further refreshing will result in a soft-ban.

## To-Do List
  * ~~~Comment parts of the code so that it can be used as a learning tool.~~~
  * ~~~Add in the abililty to manually solve captchas if desired.~~~
  * ~~~Adjust terminal coloring for Windows.~~~
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

## Common Curiosities
  * Variant Inventory vs. Client Inventory - Client inventory provides the lastest inventory for a given product (provided that the clientId is correct). The variant inventory does not reflect the latest inventory numbers - it has been observed to reflect the inventory on product release.  
