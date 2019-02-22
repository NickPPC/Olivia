import argparse
import logging
import traceback
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import json
import navigation.connection as connection
import utils
from utils import get_driver as driver
import logic.scheduler as scheduler

log = utils.get_module_logger(__name__)


def init_driver(config, no_display):
    profile = webdriver.FirefoxProfile()

    if no_display:
        #Block images
        profile.set_preference("permissions.default.image", 2)

    driver = webdriver.Firefox(firefox_profile=profile)
    utils.set_driver(driver)

    connection.connect(config)

    return driver

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--display", action="store_true", help="set display of what is happening")
parser.add_argument("-m", "--manual", action="store_true", help="Manual mode, does not start scheduler")
parser.add_argument("-f", "--configFile", help="path to the JSON config file", default='config.json')


def run(args):

    init_driver(config, no_display)
    time.sleep(2)

    if not args.manual:
        masterScheduler = scheduler.MasterScheduler(config)
        # State when connecting
        log.info(masterScheduler.empire)
        masterScheduler.run()



if __name__ == '__main__':

    args = parser.parse_args()
    no_display = not args.display and not args.manual

    if no_display:
        display = Display(visible=0, size=(1280, 1024))
        display.start()

    with open(args.configFile) as file:
        config = json.load(file)

    retry_count = 5

    while(retry_count > 0):
        try:
            run(args)
            retry_count = 0
        except Exception as e:
            log.error('Something went very wrong : {}\n{}'.format(str(e), traceback.format_exc()))
            driver().quit()
            retry_count -= 1

    if no_display:
        display.stop()
        driver().quit()

    


