import logging

log = logging.getLogger(__name__)


driver = None
def navigate_to_tab(tabName):
    tab = None
    menu = driver.find_element_by_id('menuTable')

    for element in menu.find_elements_by_tag_name('a'):
        try:
            if tabName in element.get_attribute('href'):
                tab = element
        except:
            pass

    tab.click()

def navigate_to_overview():
    navigate_to_tab('overview')

def navigate_to_galaxy():
    navigate_to_tab('galaxy')

def navigate_to_planet(planetName):

    planetLinks = driver.find_element_by_id('planetList').find_elements_by_class_name('planetlink')
    for link in planetLinks:
        if planetName in link.get_attribute('innerHTML'):
            link.click()
            return

    log.error('Planet {} not found'.format(planetName))

def list_planets():
    planetLinks = driver.find_element_by_id('planetList').find_elements_by_class_name('planetlink')
    names = [link.find_element_by_class_name('planet-name').get_attribute('innerHTML') for link in planetLinks]

    return names

