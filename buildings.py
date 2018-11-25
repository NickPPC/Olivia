import logging
import menu
import time
import planet
from utils import *
import scheduler

log = get_module_logger(__name__)


driver = None
BUILDINGS = 'buildings'
RESOURCES = 'resources'
FACILITIES = 'station'

#Resources buildings
PRODUCTION = 'building'
STORAGE = 'storage'
METAL_MINE = 'metalMine'
CRISTAL_MINE = 'cristalMine'
DEUTERIUM_MINE = 'deuteriumMine'
SOLAR_PLANT = 'solarPlant'
FISSION_PLANT = 'fissionPlant'
METAL_SILO = 'metalSilo'
CRISTAL_SILO = 'cristalSilo'
DEUTERIUM_SILO = 'deuteriumSilo'
RESOURCES_BUILDINGS = [METAL_MINE, CRISTAL_MINE, DEUTERIUM_MINE, SOLAR_PLANT,
                       FISSION_PLANT, METAL_SILO, CRISTAL_SILO, DEUTERIUM_SILO]
#Facilities
STATION_BUILDING = 'stationbuilding'
ROBOTICS_FACTORY = 'roboticsFactory'
SHIPYARD = 'shipyard'
RESEARCH_LAB = 'researchLab'
ALLIANCE_DEPOT = 'allianceDepot'
MISSILE_SILO = 'missileSilo'
NANITE_FACTORY = 'naniteFactory'
TERRAFORMER = 'terraformer'
SPACE_DOCK = 'spaceDock'
FACILITIES_BUILDINGS = [ROBOTICS_FACTORY, SHIPYARD, RESEARCH_LAB, ALLIANCE_DEPOT,
                        MISSILE_SILO,NANITE_FACTORY, TERRAFORMER, SPACE_DOCK]


buildingTranslation = {
    #Resources
    METAL_MINE : (RESOURCES, PRODUCTION, 'supply1'),
    CRISTAL_MINE : (RESOURCES, PRODUCTION, 'supply2'),
    DEUTERIUM_MINE : (RESOURCES, PRODUCTION, 'supply3'),
    SOLAR_PLANT : (RESOURCES, PRODUCTION, 'supply4'),
    FISSION_PLANT : (RESOURCES, PRODUCTION, 'supply12'),
    METAL_SILO : (RESOURCES, STORAGE, 'supply22'),
    CRISTAL_SILO : (RESOURCES, STORAGE, 'supply23'),
    DEUTERIUM_SILO : (RESOURCES, STORAGE, 'supply24'),
    #Facilities
    ROBOTICS_FACTORY : (FACILITIES, STATION_BUILDING, 'station14'),
    SHIPYARD : (FACILITIES, STATION_BUILDING, 'station21'),
    RESEARCH_LAB : (FACILITIES, STATION_BUILDING, 'station31'),
    ALLIANCE_DEPOT : (FACILITIES, STATION_BUILDING, 'station34'),
    MISSILE_SILO : (FACILITIES, STATION_BUILDING, 'station44'),
    NANITE_FACTORY : (FACILITIES, STATION_BUILDING, 'station15'),
    TERRAFORMER : (FACILITIES, STATION_BUILDING, 'station33'),
    SPACE_DOCK : (FACILITIES, STATION_BUILDING, 'station36')
}

def go_to_resources():
    menu.navigate_to_tab(RESOURCES)

def go_to_facilities():
    menu.navigate_to_tab(FACILITIES)

def go_to(buildingName):
    if buildingTranslation[buildingName][0] == RESOURCES:
        go_to_resources()
    elif buildingTranslation[buildingName][0] == FACILITIES:
        go_to_facilities()

def extract_level_building(buildingName):

    text = driver.find_element_by_id(buildingTranslation[buildingName][1]) \
        .find_element_by_class_name(buildingTranslation[buildingName][2]) \
        .find_element_by_class_name('level').get_attribute('innerHTML').strip()

    return level_extraction(text)

def extract_resources_buildings_level(planet):
    go_to_resources()
    for building in RESOURCES_BUILDINGS:
        planet.set_building_level(building, extract_level_building(building))

def extract_facilities_buildings_level(planet):
    go_to_facilities()
    for building in FACILITIES_BUILDINGS:
        planet.set_building_level(building, extract_level_building(building))

class BuildingScheduler():

    nextTimeAvailable = 0

    def __init__(self, planetName):
        self.planetName = planetName
        self.updateTimeAvailability()

    def updateTimeAvailability(self):
        menu.navigate_to_overview()
        try:
            timeLeft = driver.find_element_by_id('Countdown').get_attribute('innerHTML')
            self.nextTimeAvailable = time.time() + formatted_time_to_seconds(timeLeft)
        except Exception as e:
            log.warn('Exception {} : {}'.format(type(e).__name__, str(e)))

    # def waitUntilConstructionSlotAvailable(self):
    #     if not self.isConstructionSlotAvailable():
    #         waitTime = int(self.nextTimeAvailable - time.time() + 3)
    #         log.info('Waiting {} before next construction'.format(seconds_to_formatted_time(waitTime)))
    #         time.sleep(waitTime)

    def isConstructionSlotAvailable(self):
        return time.time() > self.nextTimeAvailable


    def clickBuildingElement(self, buildingName):

        go_to(buildingName)

        buildingElement = driver.find_element_by_id(buildingTranslation[buildingName][1]) \
            .find_element_by_class_name(buildingTranslation[buildingName][2])
        if buildingTranslation[buildingName][0] == RESOURCES:
            buildingElement.find_element_by_id('details').click()
        elif buildingTranslation[buildingName][0] == FACILITIES:
            buildingElement.find_element_by_id('details' + buildingTranslation[buildingName][2][-2:]).click()

    def getBuildingCost(self, buildingName=None):

        #If buildingName is None it means the proper building was already clicked
        if buildingName is not None:
            self.clickBuildingElement(buildingName)
            time.sleep(2)
        costList = driver.find_element_by_id('costs')
        return cost_extraction(costList)



    def upgrade_building(self, buildingName):

        if buildingName not in buildingTranslation:
            return scheduler.Event(scheduler.Event.ERROR, 0, self.planetName, 'Building is not valid')

        if not self.isConstructionSlotAvailable():
            return scheduler.Event(scheduler.Event.ERROR, 0, self.planetName, 'No construction slot')

        try:

            self.clickBuildingElement(buildingName)
            time.sleep(3)
            cost = self.getBuildingCost()

            driver.find_element_by_class_name('build-it').click()
            #TODO: improve by using construction time extracted when building
            self.updateTimeAvailability()

            log.info('{} construction started for {} metal, {} cristal and {} deuterium'.format(buildingName,
                                                                         cost[METAL], cost[CRISTAL], cost[DEUTERIUM]))
            return scheduler.Event(scheduler.Event.BUILDING_IN_PROGRESS, self.nextTimeAvailable - time.time(), self.planetName, buildingName)
        except Exception as e:
            log.error('Impossible to upgrade this building {} on {}\n {} : {}'.format(buildingName, self.planetName, type(e).__name__, str(e)))
            return scheduler.Event(scheduler.Event.ERROR, 0, self.planetName, 'Impossible to upgrade this building, {}'.format(str(e)))


    def __str__(self):
        return '{} : Next building slot available in {}'.\
            format(self.planetName, seconds_to_formatted_time(self.nextTimeAvailable - time.time()))
