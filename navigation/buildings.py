import logging
import navigation.menu as menu
import time
from utils import get_driver as driver

from utils import *
from model.buildings import *
from model.events import Event

log = get_module_logger(__name__)


def go_to_resources():
    menu.navigate_to_tab(RESOURCES)

def go_to_facilities():
    menu.navigate_to_tab(FACILITIES)

def go_to(buildingName):
    if buildingTranslation[buildingName][0] == RESOURCES:
        go_to_resources()
    elif buildingTranslation[buildingName][0] == FACILITIES:
        go_to_facilities()

def _extract_level_building(buildingName):

    text = driver().find_element_by_id(buildingTranslation[buildingName][1]) \
        .find_element_by_class_name(buildingTranslation[buildingName][2]) \
        .find_element_by_class_name('level').get_attribute('innerHTML').strip()

    return level_extraction(text)

def extract_resources_buildings_level(planetName):
    menu.navigate_to_planet(planetName)

    go_to_resources()
    building_levels = {}
    for building in RESOURCES_BUILDINGS:
        building_levels[building] = _extract_level_building(building)

    log.debug('Resources building levels extracted for {}'.format(planetName))
    return building_levels
        

def extract_facilities_buildings_level(planetName):
    menu.navigate_to_planet(planetName)

    go_to_facilities()
    building_levels = {}
    for building in FACILITIES_BUILDINGS:
        building_levels[building] = _extract_level_building(building)

    log.debug('Facilities building levels extracted for {}'.format(planetName))
    return building_levels


def getNextTimeAvailability(planetName):
    menu.navigate_to_planet(planetName)
    menu.navigate_to_overview()

    try:
        timeLeft = driver().find_element_by_id('Countdown').get_attribute('innerHTML')
        return time.time() + formatted_time_to_seconds(timeLeft)
    except Exception as e:
        log.warn('Exception {} : {}. Discard if no construction in progress'.format(type(e).__name__, str(e)))
        return 0

def get_in_progress_building(planet_name):
    menu.navigate_to_planet(planet_name)
    menu.navigate_to_overview()

    try:
        building_overview = driver().find_elements_by_class_name('content-box-s')[0]
        in_progres = building_overview.find_element_by_class_name('first')
        cancel_link = in_progres.find_elements_by_tag_name('a')[0]
        cancel_action = cancel_link.get_attribute('onClick')
        log.debug(cancel_action)
        # 3 numbers after 'cancelProduction(' (17 letters)
        item_id = cancel_action[17:19].strip(',')

        x = - len(item_id)
        for building in buildingTranslation:
            (_, _, name) = buildingTranslation[building]
            if item_id in name[x:]:
                return building

        log.error('building not identified: {}'.format(item_id))
        return None
    except Exception as e:
        log.warn('Exception {} : {}. Discard if no construction in progress'.format(type(e).__name__, str(e)))
        return None

def _clickBuildingElement(buildingName):

    go_to(buildingName)

    buildingElement = driver().find_element_by_id(buildingTranslation[buildingName][1]) \
        .find_element_by_class_name(buildingTranslation[buildingName][2])
    if buildingTranslation[buildingName][0] == RESOURCES:
        buildingElement.find_element_by_id('details').click()
    elif buildingTranslation[buildingName][0] == FACILITIES:
        buildingElement.find_element_by_id('details' + buildingTranslation[buildingName][2][-2:]).click()

def getBuildingCost(planetName, buildingName):
    menu.navigate_to_planet(planetName)
    go_to(buildingName)

    _clickBuildingElement(buildingName)
    time.sleep(2)
    return _get_current_building_cost()
    
def _get_current_building_cost():
    costList = driver().find_element_by_id('costs')
    return cost_extraction(costList)


def upgrade_building(planetName, buildingName):

    if buildingName not in buildingTranslation:
        return Event(Event.ERROR, 0, planetName, 'Building is not valid')

    menu.navigate_to_planet(planetName)
    go_to(buildingName)

    try:

        _clickBuildingElement(buildingName)
        time.sleep(3)
        cost = _get_current_building_cost()

        driver().find_element_by_class_name('build-it').click()
        #TODO: improve by using construction time extracted when building

        log.info('{} construction started for {} metal, {} cristal and {} deuterium'.format(buildingName,
                                                                        cost[METAL], cost[CRISTAL], cost[DEUTERIUM]))
        return Event(Event.BUILDING_IN_PROGRESS, getNextTimeAvailability(planetName) - time.time(), planetName, buildingName)
    except Exception as e:
        log.error('Impossible to upgrade this building {} on {}\n {} : {}'.format(buildingName, planetName, type(e).__name__, str(e)))
        return Event(Event.ERROR, 0, planetName, 'Impossible to upgrade this building, {}'.format(str(e)))
