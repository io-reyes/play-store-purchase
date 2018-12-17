import argparse
import logging
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)
my_dir = os.path.dirname(os.path.realpath(__file__))

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('paidlist', help='Path to file containing list of paid apps to purchase, one package name per line')
    parser.add_argument('profile', help='Path to Firefox profile already logged into the purchasing account')
    parser.add_argument('password', help='Password for the purchasing account')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')

    return parser.parse_args()

def _parse_paid_list(paid_file):
    logger.info('Parsing paid list file %s' % paid_file)

    paid_list = []
    with open(paid_file, 'r') as f:
        paid_list = [x.strip() for x in f.readlines()]

    logger.info(paid_list)
    logger.info('Read %d lines' % len(paid_list))
    return paid_list

def _buy(paid_list, profile_dir, password, seconds_between=20):
    geckodriver = os.path.join(my_dir, 'geckodriver', 'geckodriver-linux64')
    logger.info('Using geckodriver %s' % geckodriver)

    profile = webdriver.FirefoxProfile(profile_directory=profile_dir)
    logger.info('Using profile %s' % profile.path)

    with webdriver.Firefox(executable_path=geckodriver, firefox_profile=profile) as driver:
        for app in paid_list:
            play_store_page = 'https://play.google.com/store/apps/details?id=%s' % app
            logger.info('Loading %s' % play_store_page)
            driver.get(play_store_page)

            try:
                buy_button = driver.find_element_by_xpath("//button[contains(@aria-label, 'Buy')]")
                logger.info('Clicking the first Buy button for %s' % app)
                buy_button.click()

                purchase_iframe = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, "//iframe[starts-with(@src, 'https://play.google.com/store/epurchase')]")))
                logger.info('Found the purchasing iframe')
                driver.switch_to.frame(purchase_iframe)

                continue_button = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, 'purchase-ok-button')))
                logger.info('Clicking the Continue button for %s' % app)
                continue_button.click()

                buy_button_2 = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, 'loonie-purchase-ok-button')))
                logger.info('Clicking the second Buy button for %s' % app)
                buy_button_2.click()

                driver.switch_to.default_content()
                password_field = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@type='password' and @aria-label='Enter your password']"))) 
                logger.info('Entering the password')
                password_field.send_keys(password)
                password_field.send_keys(Keys.ENTER)

                logger.info('Sleeping for %d seconds after successful purchase' % seconds_between)
                time.sleep(seconds_between)

            except Exception as e:
                logger.exception('Exception buying %s' % app)

        driver.close()

if __name__ == '__main__':
    args = _parse_args()

    if(args.verbose):
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig()

    paid_list = _parse_paid_list(args.paidlist)
    _buy(paid_list, args.profile, args.password)

