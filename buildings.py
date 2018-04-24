import menu
import time
import planet

driver = None
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

    while '<' in text:
        i = text.find('<')
        j = text.find('>')
        if i == 0:
            text = text[j + 1:]
            text = text[text.find('>') + 1:]
        else:
            text = text[:i - 1]
        text.strip()
    return int(text)

def extract_resources_buildings_level(planet):
    go_to_resources()
    # update_planet_resources(planet)
    # Production
    planet.metalMineLevel = extract_level_building(METAL_MINE)
    planet.cristalMineLevel = extract_level_building(CRISTAL_MINE)
    planet.deuteriumMineLevel = extract_level_building(DEUTERIUM_MINE)
    planet.solarPlantLevel = extract_level_building(SOLAR_PLANT)
    planet.fissionPlantLevel = extract_level_building(FISSION_PLANT)
    # Storage
    planet.metalSiloLevel = extract_level_building(METAL_SILO)
    planet.cristalSiloLevel = extract_level_building(CRISTAL_MINE)
    planet.deuteriumSiloLevel = extract_level_building(DEUTERIUM_SILO)

def extract_facilities_buildings_level(planet):
    go_to_facilities()
    planet.roboticsFactory = extract_level_building(ROBOTICS_FACTORY)
    planet.shipyard = extract_level_building(SHIPYARD)
    planet.researchLab = extract_level_building(RESEARCH_LAB)
    planet.allianceDepot = extract_level_building(ALLIANCE_DEPOT)
    planet.missileSilo = extract_level_building(MISSILE_SILO)
    planet.naniteFactory = extract_level_building(NANITE_FACTORY)
    planet.terraformer = extract_level_building(TERRAFORMER)
    planet.spaceDock = extract_level_building(SPACE_DOCK)



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

    def __init__(self, planet, goals):
        self.planet = planet
        self.goals = goals
        self.updateTimeAvailability()

    def updateTimeAvailability(self):
        menu.navigate_to_overview()
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

    def waitUntilConstructionSlotAvailable(self):
        if not self.isConstructionSlotAvailable():
            waitTime = int(self.nextTimeAvailable - time.time() + 3)
            print('Waiting {} s before next construction'.format(waitTime))
            time.sleep(waitTime)

    def isConstructionSlotAvailable(self):
        return time.time() > self.nextTimeAvailable

    #TODO
    def isConstructionAffordable(self):
        self.planet.update_planet_resources()
        return True

    def isConstructionPossible(self):
        return self.isConstructionSlotAvailable() and self.isConstructionAffordable()

    def clickBuildingElement(self, buildingName):

        go_to(buildingName)

        buildingElement = driver.find_element_by_id(buildingTranslation[buildingName][1]) \
            .find_element_by_class_name(buildingTranslation[buildingName][2])
        if buildingTranslation[buildingName][0] == RESOURCES:
            buildingElement.find_element_by_id('details').click()
        elif buildingTranslation[buildingName][0] == FACILITIES:
            buildingElement.find_element_by_id('details' + buildingTranslation[buildingName][2][-2:]).click()

    def getBuildingCost(self, buildingName=None):

        if buildingName is not None:
            self.clickBuildingElement(buildingName)
            time.sleep(2)
        cost = {planet.METAL : 0, planet.CRISTAL : 0, planet.DEUTERIUM : 0}
        costList = driver.find_element_by_id('costs')
        try:
            cost[planet.METAL] = costList.find_element_by_class_name('metal').find_element_by_class_name('cost').get_attribute('innerHTML')
        except:
            pass
        try:
            cost[planet.CRISTAL] = costList.find_element_by_class_name('crystal').find_element_by_class_name('cost').get_attribute('innerHTML')
        except:
            pass
        try:
            cost[planet.DEUTERIUM] = costList.find_element_by_class_name('deuterium').find_element_by_class_name('cost').get_attribute('innerHTML')
        except:
            pass

        return cost



    def upgrade_building(self, buildingName):

        if buildingName not in buildingTranslation:
            print('Error, building is not valid')
            return

        self.waitUntilConstructionSlotAvailable()

        #TODO: in scheduler deal with no money case
        if self.isConstructionPossible():

            self.clickBuildingElement(buildingName)
            time.sleep(3)
            cost = self.getBuildingCost()

            driver.find_element_by_class_name('build-it').click()
            #TODO: improve by using construction time extracted when building
            self.updateTimeAvailability()

            print('{} construction started for {}'.format(buildingName, cost))
        else:
            print('Impossible to upgrade this building')

    def __str__(self):
        return ', '.join(map(str, self.goals))
