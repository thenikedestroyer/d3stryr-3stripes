# Manual Token Harvesting
**ESSENTIAL** Adding dev.adidas.com to your hosts file. This step only needs to be done once on your machine. 

0.  Type (or copy & paste) the following command below into the terminal window and then hit enter:

   Mac
   ```
   echo '127.0.0.1 dev.adidas.com' | sudo tee -a /etc/hosts > /dev/null && echo DONE
   ```
   
   It will prompt you for your password. Enter it in. It will not show you your password as you enter it in. But if you enter it in correctly then you should see:
   
   ```
   DONE
   ```
   Windows
   
   Run cmd as an administrator and type/copy & paste:
   ```
   (echo. && echo 127.0.0.1 dev.adidas.com) >> C:\Windows\System32\drivers\etc\hosts
   ```
   

Instructions for manual token harvesting.

1.  Open up `config.cfg` with a text editor and provide the necessary values for the `[harvest]` section:
   *  `manuallyHarvestTokens` - must be set to `True` if you want to turn on manual token harvesting.
   *  `numberOfTokens` - set the number of tokens you must correctly harvest before the script start adding-to-cart.
   *  `harvestDomain` - the domain that we are spoofing on 127.0.0.1 (localhost). Leave this as `dev.adidas.com`
   *  `phpServerPort` - the PHP server port.
   
2.  You must launch the php server from within the `d3stryr-3stripes` or `d3stryr-3stripes-master` folder:

    Mac/Linux
    ```
    cd d3stryr-3stripes-master
    php -S dev.adidas.com:8000
    ```
    
    Windows
	
	PHP is not installed by default on windows. Download the latest version [here](http://windows.php.net/download)
    After you've downloaded the zip, create a folder called PHP in "C:\Program Files" and drag in the contents
	of the downloaded zip. 
	Now, go to the start menu and type
	
	"Edit environmental variables for your account"
	
	Now a window should appear with the title "Environment Variables"
	In the table at the top, there should be a variable called PATH.
	Select it and click edit. At the very end, append the path of the folder you put PHP, for example:
	C:\Program Files\PHP.
	After you have added that, press OK. Now the PHP folder will be included in your PATH variable.
	Open up a new command prompt, and type the following:
	```
	cd C:\whatever\path\to\d3stryr-3stripes
    php -S dev.adidas.com:8000
	```

3.  Open another terminal window and launch the `d3stryr-3stripes.py` script.

    ```
    ./d3stryr-3stripes.py
    ```
	(Use backslash '\' for Windows)
	
4.  The script should automatically activate the captcha widget.  If it does not then click on the `I'm not a robot` checkbox.
5.  Solve the captcha and click verify.
6.  The script should automatically click the submit button once it finds the green checkmark. If it does not then it will just continue on and check to see if the token is currently present on the page.
