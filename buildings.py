import menu
import time
from planet import update_planet_resources

buildingTranslation = {'metalMine' : 'supply1',
                           'cristalMine' : 'supply2',
                           'deuteriumMine' : 'supply3',
                           'solarPlant' : 'supply4'}

def go_to_resources(driver):
    menu.navigate_to_tab(driver, 'resources')

def extract_resources_buildings_level(driver, planet):
    update_planet_resources(driver, planet)
    buildingsList = driver.find_element_by_id('building')
    planet.metalMineLevel = int(buildingsList.find_element_by_class_name('supply1')\
        .find_element_by_class_name('level').get_attribute('innerHTML').split('>')[2].strip())
    planet.cristalMineLevel = int(buildingsList.find_element_by_class_name('supply2') \
        .find_element_by_class_name('level').get_attribute('innerHTML').split('>')[2].strip())
    planet.deuteriumMineLevel = int(buildingsList.find_element_by_class_name('supply3') \
        .find_element_by_class_name('level').get_attribute('innerHTML').split('>')[2].strip())
    planet.solarPlantLevel = int(buildingsList.find_element_by_class_name('supply4') \
        .find_element_by_class_name('level').get_attribute('innerHTML').split('>')[2].strip())
    planet.fissionPlantLevel = int(buildingsList.find_element_by_class_name('supply12') \
        .find_element_by_class_name('level').get_attribute('innerHTML').split('>')[2].strip())
    storageList = driver.find_element_by_id('storage')
    planet.metalSiloLevel = int(storageList.find_element_by_class_name('supply22')\
        .find_element_by_class_name('level').get_attribute('innerHTML').split('>')[2].strip())
    planet.cristalSiloLevel = int(storageList.find_element_by_class_name('supply23') \
        .find_element_by_class_name('level').get_attribute('innerHTML').split('>')[2].strip())
    planet.deuteriumSiloLevel = int(storageList.find_element_by_class_name('supply24') \
        .find_element_by_class_name('level').get_attribute('innerHTML').split('>')[2].strip())

def upgrade_building(driver, buildingName):


    if buildingName not in buildingTranslation:
        print('Error, building is not valid')
        return

    buildingsList = driver.find_element_by_id('building')
    buildingsList.find_element_by_class_name(buildingTranslation[buildingName]).find_element_by_id('details').click()
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

    def __init__(self, driver, goals):
        self.goals = goals
        self.updateTimeAvailability(driver)

    def updateTimeAvailability(self, driver):
        menu.navigate_to_overview(driver)
        try:
            timeLeft = driver.find_element_by_id('Countdown')
            #Parsing
            days = int(timeLeft.split('d')[0])
            hours = int(timeLeft.split('d')[1].split('h')[0])
            minutes = int(timeLeft.split('d')[1].split('h')[1].split('m')[0])
            seconds = int(timeLeft.split('d')[1].split('h')[1].split('m')[1].split('s')[0])
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
