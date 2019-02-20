import argparse
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import json
import navigation.connection as connection
import utils
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



if __name__ == '__main__':

    args = parser.parse_args()
    no_display = not args.display and not args.manual

    if no_display:
        display = Display(visible=0, size=(1280, 1024))
        display.start()

    with open(args.configFile) as file:
        config = json.load(file)

    driver = init_driver(config, no_display)
    time.sleep(5)
    # Closing first tab
    del driver.window_handles[0]
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    driver.close()
    time.sleep(2)
    # Focusing on open tab
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(2)

    #Removing ad
    try:
        cloaseAdZone = driver.find_element_by_class_name('openX_int_closeButton')
        closeAdButton = cloaseAdZone.find_element_by_tag_name('a')
        closeAdButton.click()
    except:
        pass


    try:
        if not args.manual:
            masterScheduler = scheduler.MasterScheduler(config)
            # State when connecting
            log.info(masterScheduler.empire)
            masterScheduler.run()


        if no_display:
            driver.quit()
            display.stop()

    except Exception as e:
        log.error('Something went very wrong : {}'.format(str(e)))
        driver.quit()
