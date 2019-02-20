import time
import navigation.menu as menu
from utils import *
from utils import get_driver as driver
from selenium.webdriver.common.action_chains import ActionChains
import logic.scheduler as scheduler

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

    print(systems)

    for i in galaxies:
        for j in systems:
            g = current_galaxy + i
            s = current_system + j
            if g > 0 and g <= 9 and s > 0 and s < 500:
                to_explore.append((g, s))

    print(to_explore)

    results = []
    for (g, s) in to_explore:
        results.extend(scan_system(g, s))

    results = results.sort(key= lambda x: x[1])
    print('\n'.join(map(str,results)))

    return results

def scan_system(galaxy, system):
    print('Preparing to explore {}:{}'.format(galaxy, system))
    current_address = get_current_address()
    print(current_address)
    if current_address[0] != galaxy or current_address[1] != system:
        go_to_address(galaxy, system)

    planets_found = []

    table = driver().find_elements_by_tag_name('tbody')[0]
    rows = table.find_elements_by_tag_name('tr')
    galaxy_tooltips = driver().find_elements_by_class_name('galaxyTooltip')
    player_details = []
    for gt in galaxy_tooltips:
        if 'player' in gt.get_attribute('id'):
            player_details.append(gt)

    # print(player_details)

    i = 0
    for row in rows:
        if 'empty_filter' not in row.get_attribute('class') and i < len(player_details):
            try:
                elements = row.find_elements_by_tag_name('td')
                planet_address = '{}:{}:{}'.format(galaxy, system, elements[0].get_attribute('innerHTML'))
                # print(player_details[i].get_attribute('innerHTML'))
                rank_elements = player_details[i].find_elements_by_class_name('rank')
                # print(rank_elements)
                if rank_elements:
                    player_ranking = rank_elements[0].find_elements_by_tag_name('a')[0]\
                        .get_attribute('innerHTML')
                    planets_found.append((planet_address, player_ranking))
                    i += 1

            except Exception as e:
                log.warn('Problem exploring {}:{} : {}'.format(galaxy, system, str(e)))

    log.debug('{} planets found at {}:{}'.format(str(len(planets_found)), galaxy, system))

    return planets_found



def get_current_address():
    galaxy = driver().find_element_by_id('galaxy_input').get_attribute('value')
    system = driver().find_element_by_id('system_input').get_attribute('value')
    return (int(galaxy), int(system))

def go_to_address(galaxy, system):
    driver().find_element_by_id('galaxy_input').send_keys(str(galaxy))
    driver().find_element_by_id('system_input').send_keys(str(system))
    buttons = driver().find_elements_by_class_name('btn_blue')
    buttons[0].click()
    # for i in range(len(buttons)):
    #     if 'Go' in buttons[i].get_attribute('innerHTML'):
    #         buttons[i].click()
