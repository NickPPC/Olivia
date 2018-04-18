import menu
import time
from agent import driver

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
#Facilities
STATION_BUILDING = 'stationbuilding'
ROBOTICS_FACTORY = 'reoboticsFactory'
SHIPYARD = 'shipyard'
RESEARCH_LAB = 'researchLab'
ALLIANCE_DEPOT = 'allianceDepot'
MISSILE_SILO = 'missileSilo'
NANITE_FACTORY = 'naniteFactory'
TERRAFORMER = 'terraformer'
SPACE_DOCK = 'spaceDock'


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
    #TODO: check if already there
    menu.navigate_to_tab(RESOURCES)

def go_to_facilities():
    # TODO: check if already there
    menu.navigate_to_tab(FACILITIES)

def go_to(buildingName):
    if buildingTranslation[buildingName][0] == RESOURCES:
        go_to_resources()
    elif buildingTranslation[buildingName][0] == FACILITIES:
        go_to_facilities()

def extract_level_building(buildingName):

    text = driver.find_element_by_id(buildingTranslation[buildingName][1])\
        .find_element_by_class_name(buildingTranslation[buildingName][2]) \
        .find_element_by_class_name('level').get_attribute('innerHTML')

    if '<span' in text:
        return int(text.split('>')[2].strip())
    else:
        return int(text)


def extract_resources_buildings_level(driver, planet):
    go_to_resources()
    # update_planet_resources(driver, planet)
    #Production
    planet.metalMineLevel = extract_level_building(driver, METAL_MINE)
    planet.cristalMineLevel = extract_level_building(driver, CRISTAL_MINE)
    planet.deuteriumMineLevel = extract_level_building(driver, DEUTERIUM_MINE)
    planet.solarPlantLevel = extract_level_building(driver, SOLAR_PLANT)
    planet.fissionPlantLevel = extract_level_building(driver, FISSION_PLANT)
    #Storage
    planet.metalSiloLevel = extract_level_building(driver, METAL_SILO)
    planet.cristalSiloLevel = extract_level_building(driver, CRISTAL_MINE)
    planet.deuteriumSiloLevel = extract_level_building(driver, DEUTERIUM_SILO)

def extract_facilities_buildings_level(planet):
    go_to_facilities()
    planet.roboticsFactory = extract_level_building(driver, ROBOTICS_FACTORY)
    planet.shipyard = extract_level_building(driver,SHIPYARD)
    planet.researchLab = extract_level_building(driver, RESEARCH_LAB)
    planet.allianceDepot = extract_level_building(driver, ALLIANCE_DEPOT)
    planet.missileSilo = extract_level_building(driver, MISSILE_SILO)
    planet.naniteFactory = extract_level_building(driver, NANITE_FACTORY)
    planet.terraformer = extract_level_building(driver, TERRAFORMER)
    planet.spaceDock = extract_level_building(driver, SPACE_DOCK)

def upgrade_building(buildingName):


    if buildingName not in buildingTranslation:
        print('Error, building is not valid')
        return

    go_to(buildingName)

    buildingElement = driver.find_element_by_id(buildingTranslation[buildingName][1])\
        .find_element_by_class_name(buildingTranslation[buildingName][2])
    if buildingTranslation[buildingName][0] == RESOURCES:
        buildingElement.find_element_by_id('details').click()
    elif buildingTranslation[buildingName][0] == FACILITIES:
        buildingElement.find_element_by_id('details'+buildingTranslation[buildingName][2][-2:]).click()

    time.sleep(3)
    driver.find_element_by_class_name('build-it').click()

class BuildingGoal():

    metalCost = 0
    cristalCost = 0
    deuteriumCost = 0

    def __init__(self, planet, buildingName, level, priority=1):
        self.planet = planet
        self.buildingName = buildingName
        self.level = level
        self.priority = priority

#TODO: cascade requirement as new goal
#TODO : take into account priority
class BuildingScheduler():

    nextTimeAvailable = 0

    def __init__(self, goals):
        self.goals = goals
        self.updateTimeAvailability()

    def updateTimeAvailability(self):
        menu.navigate_to_overview(driver)
        try:
            timeLeft = driver.find_element_by_id('Countdown').get_attribute('innerHTML')
            #Parsing
            days = 0
            hours =0
            minutes = 0
            seconds = 0
            if 'd' in timeLeft:
                days = int(timeLeft.split('d')[0])
                timeLeft = timeLeft.split('d')[1]
            if 'h' in timeLeft:
                hours = int(timeLeft.split('h')[0])
                timeLeft = timeLeft.split('h')[1]
            if 'm' in timeLeft:
                minutes = int(timeLeft.split('m')[0])
                timeLeft = timeLeft.split('m')[1]
            if 's' in timeLeft:
                seconds = int(timeLeft.split('s')[0])
            self.nextTimeAvailable = time.time() + ((days * 24 + hours)*60 + minutes)*60 + seconds
        except Exception as e:
            print(str(e))


    def isConstructionSlotAvailable(self):
        return time.time() > self.nextTimeAvailable

    #TODO
    def isConstructionAffordable(self):
        return True

    def isConstructionPossible(self):
        return self.isConstructionSlotAvailable() and self.isConstructionAffordable()

    def description(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())
