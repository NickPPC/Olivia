import time

import navigation.menu as menu
from model.shipyard import SHIPYARD, DEFENSE, deviceTranslation, deviceCost
from utils import get_module_logger, get_driver as driver, level_extraction
from model.resources import METAL, CRISTAL, DEUTERIUM
from model.events import Event

log = get_module_logger(__name__)



#TODO: defense construction
#TODO: fleet construction

def _go_to_shipyard():
    menu.navigate_to_tab(SHIPYARD)

def _go_to_defense():
    menu.navigate_to_tab(DEFENSE)

def go_to(deviceName):
    if deviceTranslation[deviceName][0] == SHIPYARD:
        _go_to_shipyard()
    elif deviceTranslation[deviceName][0] == DEFENSE:
        _go_to_defense()

def extract_quantity_device(planetName, deviceName):
    menu.navigate_to_planet(planetName)
    go_to(deviceName)

    text = driver().find_element_by_id(deviceTranslation[deviceName][1]) \
        .find_element_by_class_name('level').get_attribute('innerHTML').strip()

    return level_extraction(text)

    
def getDeviceCost(deviceName, n=1):

    return {
        METAL: n * deviceCost[deviceName][0],
        CRISTAL: n * deviceCost[deviceName][1],
        DEUTERIUM: n * deviceCost[deviceName][2]
        }

def _click_device_element(deviceName):
    go_to(deviceName)

    driver().find_element_by_id(deviceTranslation[deviceName][1]).click()

def getNextTimeAvailability():
    # TODO
    return 0



def build_device(planet_name, deviceName, n):
    menu.navigate_to_planet(planet_name)
    go_to(deviceName)

    if deviceName not in deviceTranslation:
        return Event(Event.ERROR, 0, planet_name, 'Device is not valid')

    try:

        _click_device_element(deviceName)
        time.sleep(3)
        cost = getDeviceCost(deviceName, n)

        # Fill quantity
        driver().find_element_by_id('number').send_keys(str(n))
        # Start construction
        driver().find_element_by_class_name('build-it').click()

        log.info('Construction of {} {} started for {} metal, {} cristal and {} deuterium'.format(n, deviceName,
                                                        cost[METAL], cost[CRISTAL], cost[DEUTERIUM]))
        return Event(Event.SHIPYARD_CONSTRUCTION_IN_PROGRESS, getNextTimeAvailability() - time.time(), planet_name, deviceName)
    except Exception as e:
        log.error('Impossible to building {} {} on {}\n {} : {}'.format(n, deviceName,planet_name, type(e).__name__, str(e)))
        return Event(Event.ERROR, 0, planet_name, 'Impossible to build this device, {}'.format(str(e)))