import time
import navigation.menu as menu
from utils import get_driver as driver
from utils import *
from model.research import *
from model.events import Event

log = get_module_logger(__name__)


def go_to_research():
    menu.navigate_to_tab(RESEARCH)

def _extract_level_technology(techName):

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


def extract_research_level():
    go_to_research()
    research_levels = {}
    for tech in TECHNOLOGIES:
        research_levels[tech] = _extract_level_technology(tech)

    return research_levels


def getNextTimeAvailability(planetName):
    menu.navigate_to_planet(planetName)
    menu.navigate_to_overview()
    try:
        timeLeft = driver().find_element_by_id('researchCountdown').get_attribute('innerHTML')
        return time.time() + formatted_time_to_seconds(timeLeft)
    except Exception as e:
        log.warn('Exception {} : {}'.format(type(e).__name__, str(e)))
        return 0

def get_in_progress_research():
    menu.navigate_to_overview()

    try:
        research_overview = driver().find_elements_by_class_name('content-box-s')[1]
        in_progres = research_overview.find_element_by_class_name('first')
        cancel_link = in_progres.find_elements_by_tag_name('a')[0]
        cancel_action = cancel_link.get_attribute('onClick')
        log.debug(cancel_action)
        # 3 numbers after 'cancelResearch(' (15 letters)
        item_id = cancel_action[15:18]

        for research, details in researchTranslation.items():
            if item_id in details:
                return research

        log.error('research not identified: {}'.format(item_id))
        return None
    except Exception as e:
        log.warn('Exception {} : {}. Discard if no researh in progress'.format(type(e).__name__, str(e)))
        return None

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
