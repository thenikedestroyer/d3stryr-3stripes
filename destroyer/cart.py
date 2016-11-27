import json

from autocaptcha import get_token_from_2captcha
from harvester import harvest_tokens_manually
from settings import user_config
from utils import *

from jinja2 import Environment, PackageLoader

# Define template environment for Jinja2 templates
jinja_env = Environment(loader=PackageLoader('cart', 'templates'))


def process_add_to_cart(product_info):
    captcha_tokens_reversed = []
    if user_config.manuallyHarvestTokens:
        harvest_tokens_manually()
        captcha_tokens_reversed = list(reversed(captcha_tokens))
    for my_size in user_config.mySizes:
        try:
            my_size_ats = product_info['productStock'][my_size]['ATS']
            if my_size_ats == 0:
                print (d_(), x_('Add-To-Cart'), lr_('Out of Stock:', my_size))
                continue
            print (d_(), s_('Add-To-Cart'), my_size, ':', str(my_size_ats))
            pid = product_info['productStock'][my_size]['pid']

            # Check if we need to process captcha
            captcha_token = ''
            if user_config.processCaptcha:
                # See if we have any manual tokens available
                if captcha_tokens_reversed:
                    # Use a manual token
                    captcha_token = captcha_tokens_reversed.pop()
                    print (d_(), s_('Number of Tokens Left'), lb_(len(captcha_tokens_reversed)))
                else:
                    # No manual tokens to pop - so lets use 2captcha
                    captcha_token = get_token_from_2captcha()
            add_to_cart_chrome_ajax(pid, captcha_token)
        except KeyboardInterrupt:
            print (d_(), x_('KeyboardInterrupt'))
            sys.exit(exit_code)
        except:
            raise  # TODO: Log the exception to stderror/stdout instead of raising.
            print (d_(), x_('Add-To-Cart'), lr_(my_size, ':', 'Not Found'))


def add_to_cart_chrome_ajax(pid, captcha_token):
    cookie_script = ''
    cookie_script_domain_aware = ''
    if user_config.marketLocale == 'PT':
        base_atc_url = (
            'http://www.{0}/on/demandware.store/Sites-adidas-MLT-Site/{1}'
        ).format(user_config.marketDomain, user_config.market)
    else:
        base_atc_url = (
            'http://www.{0}/on/demandware.store/Sites-adidas-{1}-Site/{2}'
        ).format(user_config.marketDomain, user_config.marketLocale, user_config.market)

    atc_url = '{0}/Cart-MiniAddProduct'.format(base_atc_url)
    cart_url = base_atc_url.replace('http://', 'https://') + '/Cart-Show'
    data = {
        'masterPid': user_config.masterPid,
        'pid': pid,
        'Quantity': '1',
        'request': 'ajax',
        'responseformat': 'json',
        'sessionSelectedStoreID': 'null',
    }

    # If we are processing captcha then add to our payload.
    if user_config.processCaptcha:
        data['g-recaptcha-response'] = captcha_token

    # If we need captcha duplicate then add to our payload.
    if user_config.processCaptchaDuplicate:
        # Alter the ATC URL for the captcha duplicate case
        atc_url = '{0}?clientId={1}'.format(atc_url, user_config.clientId)
        # Add captcha duplicate  to our payload.
        data[user_config.duplicateField] = captcha_token

    # If cookies need to be set then add to our payload.
    if 'neverywhere' not in user_config.cookies:
        cookie_script = 'document.cookie="{0}domain=.adidas.com;path=/";'.format(user_config.cookies)
        cookie_script_domain_aware = 'document.cookie="{0}domain=.{1};path=/";'.format(
            user_config.cookies, user_config.marketDomain)

    # Render the ATC script
    script = jinja_env.get_template('atc_script.js').render(atc_url=atc_url, data=json.dumps(data, indent=2))

    if user_config.useInjectionMethod:
        injection_url = '{0}/Cart-MiniAddProduct?pid={1}&masterPid={2}&ajax=true'.format(
            base_atc_url, pid, user_config.masterPid)
        if user_config.processCaptcha:
            injection_url += '&g-recaptcha-response={0}'.format(captcha_token)

        # Render the injection script
        script = jinja_env.get_template('injection_script.js').render(injection_url=injection_url)

    external_script = None
    if len(user_config.scriptURL) > 0 and '.js' in user_config.scriptURL:
        # Render the external script
        external_script = jinja_env.get_template('external_script.js').render(script_url=user_config.scriptURL)
    if user_config.debug:
        print(d_(), z_('Debug:data'), o_(json.dumps(data, indent=2)))
        print(d_(), z_('Debug:script'), o_(script))
        print(d_(), z_('Debug:cookie'), o_(cookie_script))
        print(d_(), z_('Debug:cookie'), o_(cookie_script_domain_aware))
        print(d_(), z_('Debug:external'), o_(external_script))
    browser = get_chromedriver(chrome_folder_location='ChromeFolder')
    browser.delete_all_cookies()
    if user_config.useInjectionMethod:
        browser.get(cart_url)
    else:
        browser.get(base_atc_url)
    if len(cookie_script) > 0 and 'neverywhere' not in user_config.cookies:
        print (d_(), s_('Cookie Script'))
        browser.execute_script(cookie_script)
        browser.execute_script(cookie_script_domain_aware)
    if len(user_config.scriptURL) > 0 and '.js' in user_config.scriptURL:
        print (d_(), s_('External Script'))
        browser.execute_script(external_script)
    print (d_(), s_('ATC Script'))
    browser.execute_script(script)
    # time.sleep(user_config.sleeping)
    browser.get(base_atc_url + '/Cart-ProductCount')
    html_source = browser.page_source
    product_count = browser.find_element_by_tag_name('body').text.replace('"', '').strip()

    if user_config.debug:
        print(d_(), z_('Debug'), o_('Product Count: %s' % product_count))
        print(d_(), z_('Debug'), o_('\n{0}'.format(html_source)))
    if len(product_count) == 1 and int(product_count) > 0:
        results = browser.execute_script('window.location="{0}"'.format(cart_url))
        input('Press Enter to Close the Browser & Continue')
    else:
        print (d_(), x_('Product Count'), lr_(product_count))

    # Maybe the Product Count source has changed and we are unable
    # to parse correctly.
    if user_config.pauseBeforeBrowserQuit:
        input('Press Enter to Close the Browser & Continue')

    # Need to delete all the cookes for this session or else we will have the
    # previous size in cart
    browser.delete_all_cookies()
    browser.quit()
