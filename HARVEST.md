# Manual Token Harvesting
**ESSENTIAL** Adding dev.adidas.com to your hosts file. This step only needs to be done once on your machine. 

1.  Type (or copy & paste) the following command below into the terminal window and then hit enter:

   Mac
   ```
   echo '127.0.0.1 dev.adidas.com' | sudo tee -a /etc/hosts > /dev/null && echo DONE
   ```
   
   It will prompt you for your password. Enter it in. It will not show you your password as you enter it in. But if you enter it in correctly then you should see:
   
   ```
   DONE
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

    **Dont fucking ask me about Windows.** 

3.  Open another terminal window and launch the `d3stryr-3stripes.py` script.

    ```
    ./d3stryr-3stripes.py
    ```

4.  The script should automatically activate the captcha widget.  If it does not then click on the `I'm not a robot` checkbox.
5.  Solve the captcha and click verify.
6.  The script should automatically click the submit button once it finds the green checkmark. If it does not then it will just continue on and check to see if the token is currently present on the page.
