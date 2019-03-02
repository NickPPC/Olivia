from utils import get_driver as driver
import navigation.menu as menu
from model.shipyard import *
import time


def spy(galaxy, system, planetId, probes):
    return _send_fleet(galaxy, system,  planetId,{SPY_PROBE : probes}, {}, 'missionButton6')

def transport(galaxy, system, planetId, fleet, resources):
    return _send_fleet(galaxy, system,  planetId, fleet, resources, 'missionButton3')

def attack(galaxy, system, planetId, fleet):
    return _send_fleet(galaxy, system,  planetId, fleet, {}, 'missionButton1')

# TODO: have it return an event
def _send_fleet(galaxy, system, planetId, fleet, resources, action_id):
    menu.navigate_to_fleet()
    time.sleep(0.05)
    _select_fleet(fleet)
    time.sleep(0.05)
    _select_destination(galaxy, system, planetId)
    time.sleep(0.05)

    driver().find_element_by_id(action_id).click()
    for resource_type in resources:
        driver().find_element_by_id(resource_type).send_keys(str(resources[resource_type]))

    driver().execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver().find_element_by_id('start').click()


def _select_fleet(fleet):
    for ship in fleet:
        if fleet[ship] != 0:
            driver().find_element_by_id('ship_' + deviceTranslation[ship][1][-3:]).send_keys(str(fleet[ship]))
    
    driver().execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver().find_element_by_id('continue').click()

def _select_destination(galaxy, system, planetId):
    driver().find_element_by_id('galaxy').send_keys(str(galaxy))
    driver().find_element_by_id('system').send_keys(str(system))
    driver().find_element_by_id('position').send_keys(str(planetId))
    driver().execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver().find_element_by_id('continue').click()

    
def get_fleet_numbers():
    menu.navigate_to_fleet()
    slots_text = driver().find_element_by_id('slots').find_elements_by_class_name('advice')[0].get_attribute('innerHTML')
    slots_text = slots_text.split('>')[2]
    current_fleet = int(slots_text.split('/')[0])
    max_fleet = int(slots_text.split('/')[1])
    return (current_fleet, max_fleet)

def extract_flights():
    #TODO
    pass