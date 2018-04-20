import argparse
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

#TODO:logging


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--display", action="store_true", help="set display of what is happening")


if __name__ == '__main__':

    args = parser.parse_args()

    if not args.display:
        display = Display(visible=0, size=(800, 600))
        display.start()

    with open('config.json') as file:
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
    empire = planet.Empire()
    planet.generate_planet(empire)
    print(empire.description())


    buildingScheduler = buildings.BuildingScheduler([])
    print(buildingScheduler.description())
    # buildingScheduler.waitUntilConstructionSlotAvailable()
    # buildings.upgrade_building(buildings.SHIPYARD)
    # buildingScheduler.updateTimeAvailability()
    buildingScheduler.waitUntilConstructionSlotAvailable()
    buildings.upgrade_building(buildings.SOLAR_PLANT)
    buildingScheduler.updateTimeAvailability()
    buildingScheduler.waitUntilConstructionSlotAvailable()
    buildings.upgrade_building(buildings.CRISTAL_MINE)
    buildingScheduler.updateTimeAvailability()
    buildingScheduler.waitUntilConstructionSlotAvailable()
    buildings.upgrade_building(buildings.RESEARCH_LAB)
    # buildingScheduler.updateTimeAvailability()
    # buildingScheduler.waitUntilConstructionSlotAvailable()
    # buildings.upgrade_building(buildings.RESEARCH_LAB)
    # buildingScheduler.updateTimeAvailability()
    # buildingScheduler.waitUntilConstructionSlotAvailable()
    # buildings.upgrade_building(buildings.METAL_MINE)
    # buildingScheduler.updateTimeAvailability()
    # buildingScheduler.waitUntilConstructionSlotAvailable()
    # buildings.upgrade_building(buildings.SOLAR_PLANT)







    if not args.display:
        driver.quit()

