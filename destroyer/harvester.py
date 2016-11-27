import _thread
import time

from flask import Flask, request, render_template
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from settings import user_config, captcha_tokens
from utils import d_, s_, x_, lb_, lr_, get_chromedriver

harvest_server = Flask(__name__)


@harvest_server.route('/', methods=['GET', 'POST'])
def manual_harvest():
    """
    View for manual harvesting.
    """
    sitekey = user_config.sitekey
    token = request.form.get('g-recaptcha-response', '')
    return render_template('harvester.html', sitekey=sitekey, token=token)


def harvest_tokens_manually():
    """
    Harvest tokens manually
    """
    print (d_(), s_('Manual Token Harvest'), lb_('Number of tokens harvested: %d' % len(captcha_tokens)))

    # Run the harvest server
    # XXX: This threading module is deprecated
    _thread.start_new_thread(harvest_server.run, ())

    browser = get_chromedriver(chrome_folder_location='ChromeTokenHarvestFolder', window_size=['640,640'])
    url = 'http://{0}:{1}{2}'.format(user_config.harvestDomain, 5000, '')  # Flask runs on port 5000 by default.
    while len(captcha_tokens) < user_config.numberOfTokens:
        browser.get(url)
        main_window = browser.current_window_handle

        try:
            activate_captcha(driver=browser)
        except:
            print (d_(), x_('Page Load Failed'), lr_('Falling back to 2captcha'))
            browser.quit()
            return

        check_solution(driver=browser, main_window=main_window)
        token = get_token(driver=browser, main_window=main_window)
        if token is not None:
            if len(captcha_tokens) == 0:
                start_time = time.time()
            captcha_tokens.append(token)
            print (d_(), s_('Token Added'))
            print (d_(), s_('Manual Token Harvest'), lb_('Number of tokens harvested: %d' % len(captcha_tokens)))
        current_time = time.time()
        elapsed_time = current_time - start_time
        print (d_(), s_('Total Time Elapsed'), lb_(round(elapsed_time, 2), 'seconds'))
    browser.quit()


def activate_captcha(driver):
    """
    Activate the catpcha widget
    """
    iframe = driver.find_element_by_css_selector('iframe[src*="api2/anchor"]')
    driver.switch_to_frame(iframe)
    try:
        checkbox = WebDriverWait(driver, user_config.sleeping).until(
            expected_conditions.presence_of_element_located((By.ID, 'recaptcha-anchor')))
    except:
        try:
            checkbox = WebDriverWait(driver, user_config.sleeping).until(
                expected_conditions.presence_of_element_located((By.ID, 'recaptcha-anchor')))
        except:
            print (d_(), x_('Activate Captcha'), lr_('Failed to find checkbox'))
    checkbox.click()


def check_solution(driver, main_window):
    """
    Check to see if we solved the captcha
    """
    solved = False
    while not solved:
        driver.switch_to.window(main_window)
        try:
            iframe = driver.find_element_by_css_selector('iframe[src*="api2/anchor"]')
        except:
            print (d_(), x_('Check Solution'), lr_('Failed to find checkbox'))
            return
        driver.switch_to_frame(iframe)
        try:
            driver.find_element_by_xpath('//span[@aria-checked="true"]')
            print (d_(), s_('Check Solution'), lb_('Solved'))
            solved = True
        except:
            solved = False
        time.sleep(1)
    return solved


def get_token(driver, main_window):
    """
    We parse the token from the page
    """
    token = None
    driver.switch_to.window(main_window)
    try:
        submit = WebDriverWait(driver, user_config.sleeping).until(
            expected_conditions.presence_of_element_located((By.ID, 'submit')))
        submit.click()
        time.sleep(1)
    except:
        print (d_(), x_('Captcha Submit'), lr_('Failed to click submit'))

    token_element = driver.find_element_by_css_selector('p#token')
    token = token_element.get_attribute('value')
    if token is not None:
        print (d_(), s_('Get Token'), lb_(token))
    return token
