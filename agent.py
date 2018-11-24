import argparse
import logging
import time
from selenium import webdriver
from pyvirtualdisplay import Display
import json
import connection
import planet
import buildings
import menu
import research
import fleet
import shipyard
import scheduler
import utils

log = utils.get_module_logger(__name__)


def init_driver(config):
    driver = webdriver.Firefox()

    connection.driver = driver
    buildings.driver = driver
    planet.driver = driver
    menu.driver = driver
    research.driver = driver
    fleet.driver = driver
    shipyard.driver = driver

    connection.connect(config)


    return driver

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--display", action="store_true", help="set display of what is happening")
parser.add_argument("-m", "--manual", action="store_true", help="Manual mode, does not start scheduler")
parser.add_argument("-f", "--configFile", help="path to the JSON config file", default='config.json')



if __name__ == '__main__':

    args = parser.parse_args()

    if not args.display and not args.manual:
        display = Display(visible=0, size=(1280, 1024))
        display.start()

    with open(args.configFile) as file:
        config = json.load(file)

    driver = init_driver(config)
    time.sleep(5)
    driver.get('https://s146-us.ogame.gameforge.com/game/index.php?page=overview')


    if not args.manual:
        masterScheduler = scheduler.MasterScheduler(config)
        # State when connecting
        log.info(masterScheduler.empire)
        masterScheduler.run()


    if not args.display and not args.manual:
        driver.quit()
        display.stop()


