import time
import menu
import planet
from utils import *
import scheduler

log = get_module_logger(__name__)


driver = None

RESEARCH_PLANET = 'researchPlanet'

RESEARCH = 'research'
#Technolgies
ENERGY_TECH = 'energyTech'
LASER_TECH = 'laserTech'
ION_TECH = 'ionTech'
PLASMA_TECH = 'plasmaTech'
HYPERSPACE_TECH = 'hyperspaceTech'
COMBUSTION_DRIVE = 'combustionDrive'
PROPULSION_DRIVE = 'propulsionDrive'
HYPERSPACE_DRIVE = 'hyperspaceDrive'
ESPIONAGE_TECH = 'espionageTech'
COMPUTER_TECH = 'computerTech'
ASTROPHYSICS_TECH = 'astrophysicsTech'
INTERGALACTIC_RESEARCH_NETWORK = 'intergalacticResearchNetwork'
GRAVITON_TECH = 'gravitonTech'
WEAPONS_TECH = 'weaponsTech'
SHIELD_TECH = 'shieldTech'
ARMOR_TECH = 'armorTech'

TECHNOLOGIES = [ENERGY_TECH,LASER_TECH, ION_TECH ,PLASMA_TECH, HYPERSPACE_TECH,
                COMBUSTION_DRIVE, PROPULSION_DRIVE, HYPERSPACE_DRIVE, ESPIONAGE_TECH,
                COMPUTER_TECH, ASTROPHYSICS_TECH, INTERGALACTIC_RESEARCH_NETWORK,
                GRAVITON_TECH, WEAPONS_TECH, SHIELD_TECH, ARMOR_TECH]

researchTranslation = {
    ENERGY_TECH : 'details113',
    LASER_TECH : 'details120',
    ION_TECH : 'details121',
    PLASMA_TECH : 'details122',
    HYPERSPACE_TECH : 'details114',
    COMBUSTION_DRIVE : 'details115',
    PROPULSION_DRIVE: 'details117',
    HYPERSPACE_DRIVE: 'details118',
    ESPIONAGE_TECH : 'details106',
    COMPUTER_TECH : 'details108',
    ASTROPHYSICS_TECH : 'details124',
    INTERGALACTIC_RESEARCH_NETWORK : 'details123',
    GRAVITON_TECH : 'details199',
    WEAPONS_TECH : 'details109',
    SHIELD_TECH : 'details110',
    ARMOR_TECH : 'details111'
}


def go_to_research():
    menu.navigate_to_tab(RESEARCH)

def extract_level_technology(techName):

    text = driver.find_element_by_id(researchTranslation[techName]) \
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


def extract_research_level(empire):
    go_to_research()
    for tech in TECHNOLOGIES:
        empire.set_research_level(tech, extract_level_technology(tech))

class ResearchScheduler():

    nextTimeAvailable = 0
    lockedForUpgrade = False

    def __init__(self, planetName):
        self.planetName = planetName
        self.updateTimeAvailability()

    def updateTimeAvailability(self):
        menu.navigate_to_overview()
        try:
            timeLeft = driver.find_element_by_id('researchCountdown').get_attribute('innerHTML')
            self.nextTimeAvailable = time.time() + formatted_time_to_seconds(timeLeft)
        except Exception as e:
            log.warn('Exception {} : {}'.format(type(e).__name__, str(e)))

    # def waitUntilResearchSlotAvailable(self):
    #     if not self.isResearchSlotAvailable():
    #         waitTime = self.nextTimeAvailable - time.time() + 3
    #         print('Waiting {} s before next construction'.format(waitTime))
    #         time.sleep(waitTime)

    def isResearchSlotAvailable(self):
        return time.time() > self.nextTimeAvailable

    def clickTechElement(self, techName):
        go_to_research()
        driver.find_element_by_id(researchTranslation[techName]).click()

    def getTechCost(self, techName=None):
        if techName is not None:
            self.clickTechElement(techName)
            time.sleep(3)

        return cost_extraction(driver.find_element_by_id('costs'))

    def researchTech(self, techName):
        if techName not in researchTranslation:
            return scheduler.Event(scheduler.Event.ERROR, 0, self.planetName, 'Technology is not valid')

        if self.lockedForUpgrade:
            return scheduler.Event(scheduler.Event.RESEARCH_LAB_LOCKED, 24 * 60, self.planetName)


        if not self.isResearchSlotAvailable():
            return scheduler.Event(scheduler.Event.ERROR, 0, self.planetName, 'No construction slot')

        try:

            self.clickTechElement(techName)
            time.sleep(3)
            cost = self.getTechCost()

            driver.find_element_by_class_name('build-it').click()
            # TODO: improve by using construction time extracted when building
            self.updateTimeAvailability()
            log.info('{} research started for {} metal, {} cristal and {} deuterium'.format(techName,
                                                                                                cost[METAL],
                                                                                                cost[CRISTAL],
                                                                                                cost[DEUTERIUM]))
            return scheduler.Event(scheduler.Event.RESEARCH_IN_PROGRESS, self.nextTimeAvailable - time.time(), self.planetName,
                         techName)

        except Exception as e:
            log.error('Impossible to do this research {} on {}\n {} : {}'.format(techName, self.planetName, type(e).__name__, str(e)))
            return scheduler.Event(scheduler.Event.ERROR, 0, self.planetName, 'Impossible to research this technology, {}'.format(str(e)))
