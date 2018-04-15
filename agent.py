import argparse
import time
from selenium import webdriver
from pyvirtualdisplay import Display
import connection
import json


driver = None
config = None

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

    if not args.display:
        driver.quit()

