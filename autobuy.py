import argparse
import logging
import os
import time

from selenium import webdriver

logger = logging.getLogger(__name__)
my_dir = os.path.dirname(os.path.realpath(__file__))

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('paidlist', help='Path to file containing list of paid apps to purchase, one package name per line')
    parser.add_argument('profile', help='Path to Firefox profile already logged into the purchasing account')
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

def _buy(paid_list, profile_dir):
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
                logger.info(buy_button)
                buy_button.click()

            except Exception as e:
                logger.exception('Exception buying %s' % app)

            finally:
                time.sleep(2)

        driver.close()

if __name__ == '__main__':
    args = _parse_args()

    if(args.verbose):
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig()

    paid_list = _parse_paid_list(args.paidlist)
    _buy(paid_list, args.profile)

