import argparse
import time
from selenium import webdriver
from pyvirtualdisplay import Display
import connection
import json
import planet
import buildings


driver = None
config = None
empire = None

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
    connection.connect(config)

    #State when connecting
    empire = planet.Empire()
    planet.generate_planet(empire)
    print(empire.description())


    buildingScheduler = buildings.BuildingScheduler([])
    print(buildingScheduler.description())
    print(buildingScheduler.isConstructionSlotAvailable())
    if not buildingScheduler.isConstructionSlotAvailable():
        waitTime = buildingScheduler.nextTimeAvailable - time.time() + 3
        print('Waiting {} s before next construction'.format(waitTime))
        time.sleep(waitTime)
    buildings.upgrade_building(driver, buildings.METAL_MINE)




    if not args.display:
        driver.quit()

