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
    LIGHT_FIGHTER : (SHIPYARD, 'details204'),
    HEAVY_FIGHTER : (SHIPYARD, 'details205'),
    CRUISER: (SHIPYARD, 'details206'),
    BATTLESHIP: (SHIPYARD, 'details207'),
    BATTLECRUISER: (SHIPYARD, 'details215'),
    BOMBER: (SHIPYARD, 'details211'),
    DESTROYER: (SHIPYARD, 'details213'),
    DEATHSTAR: (SHIPYARD, 'details214'),
    SMALL_TRANSPORTER: (SHIPYARD, 'details202'),
    LARGE_TRANSPORTER: (SHIPYARD, 'details203'),
    COLONY_SHIP: (SHIPYARD, 'details208'),
    RECYCLER: (SHIPYARD, 'details209'),
    SPY_PROBE: (SHIPYARD, 'details210'),
    SOLAR_SATELLITE: (SHIPYARD, 'details212'),
    #Defense
    MISSILE_LAUCHER : (DEFENSE, 'details401'),
    LIGHT_LASER_DEFENSE: (DEFENSE, 'details402'),
    HEAVY_LASER_DEFENSE: (DEFENSE, 'details403'),
    ION_CANON: (DEFENSE, 'details404'),
    GAUSS_CANON: (DEFENSE, 'details405'),
    PLASMA_CANON: (DEFENSE, 'details406'),
    SMALL_SHIELD: (DEFENSE, 'details407'),
    LARGE_SHIELD: (DEFENSE, 'details408'),
    DEFENSE_MISSILE: (DEFENSE, 'details502'),
    ATTACK_MISSILE: (DEFENSE, 'details503'),
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
