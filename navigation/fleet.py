from utils import get_driver as driver
import navigation.menu as menu
from model.shipyard import *
#TODO: spy
#TODO: attack
#TODO: transport


def spy(galaxy, system, planetId, probes):
    menu.navigate_to_fleet()

    pass

def transport(galaxy, system, planetId, resources):
    menu.navigate_to_fleet()

    pass

def attack(galaxy, system, planetId, fleet):
    menu.navigate_to_fleet()


def _select_fleet(galaxy, system, planetId, fleet):
    for ship in fleet:
        if fleet[ship] != 0:
            driver().find_element_by_id('ship_' + deviceTranslation[ship][1][-3:]).send_keys(str(fleet[ship]))
    
    driver().find_element_by_id('continue').click()
    

