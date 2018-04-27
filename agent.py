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


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--display", action="store_true", help="set display of what is happening")
parser.add_argument("-f", "--configFile", help="path to the JSON config file", default='config.json')



if __name__ == '__main__':

    args = parser.parse_args()

    if not args.display:
        display = Display(visible=0, size=(1280, 1024))
        display.start()

    with open(args.configFile) as file:
        config = json.load(file)
    driver = webdriver.Firefox()


    connection.driver = driver
    buildings.driver = driver
    planet.driver = driver
    menu.driver = driver
    research.driver = driver
    fleet.driver = driver
    shipyard.driver = driver

    connection.connect(config)

    #State when connecting
    masterScheduler = scheduler.MasterScheduler(config)
    log.info(masterScheduler.empire)
    # masterScheduler.run()


    # masterScheduler.researchScheduler.researchTech(research.ASTROPHYSICS_TECH)
    # masterScheduler.researchScheduler.researchTech(research.ASTROPHYSICS_TECH)
    # masterScheduler.researchScheduler.researchTech(research.WEAPONS_TECH)
    # masterScheduler.researchScheduler.researchTech(research.WEAPONS_TECH)
    #
    #
    #
    #
    #
    # masterScheduler.buildingSchedulers[0].upgrade_building(buildings.CRISTAL_SILO)
    # masterScheduler.buildingSchedulers[0].upgrade_building(buildings.DEUTERIUM_SILO)
    # masterScheduler.buildingSchedulers[0].upgrade_building(buildings.SHIPYARD)




    if not args.display:
        driver.quit()
        display.stop()


