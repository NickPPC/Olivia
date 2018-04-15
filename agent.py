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
    connection.connect(driver, config)

    empire = planet.Empire()
    planet.generate_planet(driver, empire)

    print(empire.description())

    buildings.go_to_resources(driver)
    buildings.extract_resources_buildings_level(driver, empire.planets['HomeWorld'])
    print(empire.description())

    if not args.display:
        driver.quit()

