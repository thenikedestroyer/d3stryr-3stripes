import sys
import time

import requests

from settings import exit_code, user_config
from utils import d_, lb_, s_, x_, y_


def get_token_from_2captcha():
    session = requests.Session()
    session.verify = False
    session.cookies.clear()
    pageurl = 'http://www.{0}'.format(user_config.marketDomain)
    print (d_(), s_('pageurl'), lb_(pageurl))
    print (d_(), s_('sitekey'), lb_(user_config.sitekey))
    while True:
        data = {
            'key': user_config.apikey2captcha,
            'action': 'getbalance',
            'json': 1,
        }
        response = session.get(url='http://2captcha.com/res.php', params=data)
        if "ERROR_WRONG_USER_KEY" in response.text:
            print (d_(), x_('Response'), y_(response.text))
            sys.exit(exit_code)

        try:
            JSON = response.json()
        except:
            raise
            print (d_(), x_('Sleeping'), y_(user_config.sleeping, 'seconds'))
            time.sleep(user_config.sleeping)
            continue

        if JSON['status'] == 1:
            balance = JSON['request']
            print (d_(), s_('Balance'), lb_('${0}'.format(balance)))
        else:
            print (d_(), x_('Balance'))

        CAPTCHAID = None
        proceed = False
        while not proceed:
            data = {
                'key': user_config.apikey2captcha,
                'method': 'userrecaptcha',
                'googlekey': user_config.sitekey,
                'proxy': user_config.proxy2Captcha,
                'proxytype': 'HTTP',
                'pageurl': pageurl,
                'json': 1
            }
            response = session.post(url='http://2captcha.com/in.php', data=data)
            try:
                JSON = response.json()
            except:
                print (d_(), x_('Response'), y_(response.text))
                print (d_(), x_('Sleeping'), y_(user_config.sleeping, 'seconds'))
                time.sleep(user_config.sleeping)
                continue

            if JSON['status'] == 1:
                CAPTCHAID = JSON['request']
                proceed = True
                print (d_(), s_('Captcha ID'), lb_(CAPTCHAID))
            else:
                print (d_(), x_('Response'), y_(response.text))
                print (d_(), x_('Sleeping'), y_(user_config.sleeping, 'seconds'))
                time.sleep(user_config.sleeping)
        print (d_(), s_('Waiting'), '%d seconds before polling for Captcha response' % user_config.sleeping)
        time.sleep(user_config.sleeping)

        TOKEN = None
        proceed = False
        while not proceed:
            data = {
                'key': user_config.apikey2captcha,
                'action': 'get',
                'json': 1,
                'id': CAPTCHAID,
            }
            response = session.get(url='http://2captcha.com/res.php', params=data)
            JSON = response.json()
            if JSON['status'] == 1:
                TOKEN = JSON['request']
                proceed = True
                print (d_(), s_('Token ID'), lb_(TOKEN))
            else:
                print (d_(), x_('Response'), y_(response.text))
                print (d_(), x_('Sleeping'), y_(user_config.sleeping, 'seconds'))
                time.sleep(user_config.sleeping)

        data = {
            'key': user_config.apikey2captcha,
            'action': 'getbalance',
            'json': 1,
        }
        response = session.get(url='http://2captcha.com/res.php', params=data)
        JSON = response.json()
        if JSON['status'] == 1:
            balance = JSON['request']
            print (d_(), s_('Balance'), lb_('${0}'.format(balance)))
        else:
            print (d_(), x_('Balance'))
        if TOKEN is not None:
            return TOKEN
