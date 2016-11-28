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

3.  Launch the `destroyer.py` script.

    ```
    ./destroyer/destroyer.py
    ```
	(Use backslash '\' for Windows)

4.  The script should automatically activate the captcha widget.  If it does not then click on the `I'm not a robot` checkbox.
5.  Solve the captcha and click verify.
6.  The script should automatically click the submit button once it finds the green checkmark. If it does not then it will just continue on and check to see if the token is currently present on the page.
