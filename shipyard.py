import time
import menu
import planet
from utils import *
import scheduler

log = get_module_logger(__name__)


driver = None

#TODO: defense construction
#TODO: fleet construction

SHIPYARD = 'shipyard'
DEFENSE = 'defense'
#Military ships
LIGHT_FIGHTER = 'lightFighter'
HEAVY_FIGHTER = 'heavyFighter'
CRUISER = 'cruiser'
BATTLESHIP = 'battleship'
BATTLECRUISER = 'battlecruiser'
BOMBER = 'bomber'
DESTROYER = 'destroyer'
DEATHSTAR = 'deathStar'
#Civilian ships
SMALL_TRANSPORTER = 'smallTransporter'
LARGE_TRANSPORTER = 'largeTransporter'
RECYCLER = 'recycler'
SPY_PROBE = 'spyProbe'
COLONY_SHIP = 'colonyShip'
SOLAR_SATELLITE = 'solarSatellite'
#Defense
MISSILE_LAUCHER = 'missileLauncher'
LIGHT_LASER_DEFENSE = 'lightLaserDefense'
HEAVY_LASER_DEFENSE = 'heavyLaserDefense'
ION_CANON = 'ionCanon'
GAUSS_CANON = 'gaussCanon'
PLASMA_CANON = 'plasmaCanon'
SMALL_SHIELD = 'smallShield'
LARGE_SHIELD = 'largeShield'
DEFENSE_MISSILE = 'interceptionMissile'
ATTACK_MISSILE = 'interplanetarMissile'

deviceTranslation = {
    #Shipyard
    LIGHT_FIGHTER : (SHIPYARD, 'military.button1', 'details204'),
    HEAVY_FIGHTER : (SHIPYARD, 'military.button2', 'details205'),
    CRUISER: (SHIPYARD, 'military.button3', 'details206'),
    BATTLESHIP: (SHIPYARD, 'military.button4', 'details207'),
    BATTLECRUISER: (SHIPYARD, 'military.button5', 'details215'),
    BOMBER: (SHIPYARD, 'military.button6', 'details211'),
    DESTROYER: (SHIPYARD, 'military.button7', 'details213'),
    DEATHSTAR: (SHIPYARD, 'military.button8', 'details214'),
    SMALL_TRANSPORTER: (SHIPYARD, 'civil.button1', 'details202'),
    LARGE_TRANSPORTER: (SHIPYARD, 'civil.button2', 'details203'),
    COLONY_SHIP: (SHIPYARD, 'civil.button3', 'details208'),
    RECYCLER: (SHIPYARD, 'civil.button4', 'details209'),
    SPY_PROBE: (SHIPYARD, 'civil.button5', 'details210'),
    SOLAR_SATELLITE: (SHIPYARD, 'civil.button6', 'details212'),
    #Defense
    MISSILE_LAUCHER : (DEFENSE, 'defense401', 'details401'),
    LIGHT_LASER_DEFENSE: (DEFENSE, 'defense402', 'details402'),
    HEAVY_LASER_DEFENSE: (DEFENSE, 'defense403', 'details403'),
    ION_CANON: (DEFENSE, 'defense404', 'details404'),
    GAUSS_CANON: (DEFENSE, 'defense405', 'details405'),
    PLASMA_CANON: (DEFENSE, 'defense406', 'details406'),
    SMALL_SHIELD: (DEFENSE, 'defense407', 'details407'),
    LARGE_SHIELD: (DEFENSE, 'defense408', 'details408'),
    DEFENSE_MISSILE: (DEFENSE, 'defense502', 'details502'),
    ATTACK_MISSILE: (DEFENSE, 'defense503', 'details503'),
}

def go_to_shipyard():
    menu.navigate_to_tab(SHIPYARD)

def go_to_defense():
    menu.navigate_to_tab(DEFENSE)

def go_to(deviceName):
    if deviceTranslation[deviceName][0] == SHIPYARD:
        go_to_shipyard()
    elif deviceTranslation[deviceName][0] == DEFENSE:
        go_to_defense()

def extract_level_device(deviceName):

    text = driver.find_element_by_id(deviceTranslation[deviceName][1]) \
        .find_element_by_class_name('level').get_attribute('innerHTML').strip()

    return level_extraction(text)

class ShipyardScheduler():

    def __init__(self):
        pass

    def click_device_element(self, deviceName):

        go_to(deviceName)

        driver.find_element_by_id(deviceTranslation[deviceName][2]).click()

    def get_device_cost(self, deviceName=None):

        #If deviceName is None it means the proper device was already clicked
        if deviceName is not None:
            self.click_device_element(deviceName)
            time.sleep(2)
        costList = driver.find_element_by_id('costs')
        return cost_extraction(costList)

    def set_device_construction_number(self, deviceName=None, deviceNumber=0):

        #If devineName is None or deviceNumber is 0, it means the function is useless
        if (deviceName is not None) and (deviceNumber is not 0):
            self.click_device_element(deviceName)
            time.sleep(2)
            inputElement = driver.find_element_by_id('number')
            inputElement.send_keys('{}'.format(deviceNumber))
