import time
import navigation.menu as menu
from utils import get_driver as driver
from utils import *
from model.research import *
from model.events import Event

log = get_module_logger(__name__)


def go_to_research():
    menu.navigate_to_tab(RESEARCH)

def extract_level_technology(techName):

    text = driver().find_element_by_id(researchTranslation[techName]) \
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


def getNextTimeAvailability(planetName):
    menu.navigate_to_planet(planetName)
    menu.navigate_to_overview()
    try:
        timeLeft = driver().find_element_by_id('researchCountdown').get_attribute('innerHTML')
        return time.time() + formatted_time_to_seconds(timeLeft)
    except Exception as e:
        log.warn('Exception {} : {}'.format(type(e).__name__, str(e)))
        return 0


def clickTechElement(planetName, techName):
    menu.navigate_to_planet(planetName)
    go_to_research()
    driver().find_element_by_id(researchTranslation[techName]).click()

def getTechCost(planetName, techName):
    menu.navigate_to_planet(planetName)
    go_to_research()

    clickTechElement(planetName, techName)
    time.sleep(3)
    return _get_current_tech_cost()

def _get_current_tech_cost():
    return cost_extraction(driver().find_element_by_id('costs'))


def researchTech(planetName, techName):
    menu.navigate_to_planet(planetName)
    go_to_research()

    if techName not in researchTranslation:
        return Event(Event.ERROR, 0, planetName, 'Technology is not valid')

    try:

        clickTechElement(planetName, techName)
        time.sleep(3)
        cost = _get_current_tech_cost()

        driver().find_element_by_class_name('build-it').click()
        # TODO: improve by using construction time extracted when building
        log.info('{} research started for {} metal, {} cristal and {} deuterium'.format(techName,
                                                                                            cost[METAL],
                                                                                            cost[CRISTAL],
                                                                                            cost[DEUTERIUM]))
        return Event(Event.RESEARCH_IN_PROGRESS, getNextTimeAvailability(planetName) - time.time(), planetName,
                        techName)

    except Exception as e:
        log.error('Impossible to do this research {} on {}\n {} : {}'.format(techName, planetName, type(e).__name__, str(e)))
        return Event(Event.ERROR, 0, planetName, 'Impossible to research this technology, {}'.format(str(e)))
