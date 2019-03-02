import time
import navigation.menu as menu
from utils import *
from utils import get_driver as driver
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions
from model.target import Target

log = get_module_logger(__name__)

def crawl_galaxy(max_systems = 10, max_galaxy = 0):
    menu.navigate_to_galaxy()
    time.sleep(1)
    (current_galaxy, current_system) = get_current_address()
    to_explore = []

    # galaxies = list(set(list(range(max_galaxy + 1)) + ((-1) * list(range(max_galaxy + 1)))))
    # systems = list(set(list(range(max_systems + 1)) + ((-1) * list(range(max_systems + 1)))))

    galaxies = list(range((-1) * max_galaxy, max_galaxy + 1))
    systems = list(range((-1) * max_systems, max_systems + 1))

    log.debug(systems)

    for i in galaxies:
        for j in systems:
            g = current_galaxy + i
            s = (current_system + j) % 500
            if g > 0 and g <= 9 and s > 0 and s < 500:
                to_explore.append((g, s))

    log.debug(to_explore)

    results = []
    for (g, s) in to_explore:
        results.extend(scan_system(g, s))

    return results

# Scan system and return (planet_address, player_rank, inactive)
def scan_system(galaxy, system):
    log.debug('Preparing to explore {}:{}'.format(galaxy, system))
    current_address = get_current_address()
    log.debug(current_address)
    if current_address[0] != galaxy or current_address[1] != system:
        go_to_address(galaxy, system)


    try:

        planets_found = []

        table = driver().find_elements_by_tag_name('tbody')[0]
        rows = table.find_elements_by_tag_name('tr')
        galaxy_tooltips = driver().find_elements_by_class_name('galaxyTooltip')
        player_details = []
        for gt in galaxy_tooltips:
            if 'player' in gt.get_attribute('id'):
                player_details.append(gt)

        i = 0
        for row in rows:
            if 'empty_filter' not in row.get_attribute('class') and i < len(player_details):
                elements = row.find_elements_by_tag_name('td')
                planet_id = elements[0].get_attribute('innerHTML')
                # Check inactivity
                inactive = False
                if 'inactive_filter' in row.get_attribute('class'):
                    inactive = True
                rank_elements = player_details[i].find_elements_by_class_name('rank')
                if rank_elements:
                    player_ranking = rank_elements[0].find_elements_by_tag_name('a')[0]\
                        .get_attribute('innerHTML')
                    planets_found.append(Target(galaxy, system, planet_id, int(player_ranking), inactive))
                    i += 1                    
                
        log.debug('{} planets found at {}:{}'.format(str(len(planets_found)), galaxy, system))

        return planets_found
    except Exception as e:
        log.warn('Problem exploring {}:{} : {}'.format(galaxy, system, str(e)))

    return []


def get_current_address():
    galaxy = driver().find_element_by_id('galaxy_input').get_attribute('value')
    system = driver().find_element_by_id('system_input').get_attribute('value')
    return (int(galaxy), int(system))

def go_to_address(galaxy, system):
    driver().find_element_by_id('galaxy_input').send_keys(str(galaxy))
    driver().find_element_by_id('system_input').send_keys(str(system))
    buttons = driver().find_elements_by_class_name('btn_blue')
    buttons[0].click()
    time.sleep(0.3)
    # for i in range(len(buttons)):
    #     if 'Go' in buttons[i].get_attribute('innerHTML'):
    #         buttons[i].click()
