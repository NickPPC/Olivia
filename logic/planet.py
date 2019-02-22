import logging

from navigation.buildings import extract_facilities_buildings_level, extract_resources_buildings_level, get_in_progress_building
from navigation.research import  extract_research_level, get_in_progress_research
import navigation.menu as menu
from utils import get_driver as driver
from utils import *
from model.buildings import *
from model.research import *
from model.events import get_type

log = get_module_logger(__name__)


class Planet():


    def __init__(self, name):
        self.empire = None
        # Resources
        self.resources = {
            METAL: 0,
            CRISTAL: 0,
            DEUTERIUM: 0,
            ENERGY: 0
        }
        # Production
        self.production = {
            METAL: 0,
            CRISTAL: 0,
            DEUTERIUM: 0,
            ENERGY: 0
        }
        # Storage
        self.storage = {
            METAL : 0,
            CRISTAL: 0,
            DEUTERIUM: 0
        }
        # Buildings
        self._building_level = {
            # Resources buildings
            METAL_MINE: 0,
            CRISTAL_MINE: 0,
            DEUTERIUM_MINE: 0,
            SOLAR_PLANT: 0,
            FISSION_PLANT: 0,
            METAL_SILO: 0,
            CRISTAL_SILO: 0,
            DEUTERIUM_SILO: 0,
            # Facilities buildings
            ROBOTICS_FACTORY: 0,
            SHIPYARD: 0,
            RESEARCH_LAB: 0,
            ALLIANCE_DEPOT: 0,
            MISSILE_SILO: 0,
            NANITE_FACTORY: 0,
            TERRAFORMER: 0,
            SPACE_DOCK: 0
        }

        self._shipyard_locked = False
        self._shipyard_queue_empty = True
        self._building_slot_available = True

        self.name = name
        self.full_update()
       
    def update_buildings_level(self):
        building_levels = extract_resources_buildings_level(self.name)
        building_levels.update(extract_facilities_buildings_level(self.name))

        for building, level in building_levels.items():
            self.set_building_level(building, level)

        log.debug('Checking in progress construction')
        in_progress_building = get_in_progress_building(self.name)
        if in_progress_building is not None:
            self.set_building_level(in_progress_building, self.get_building_level(in_progress_building) + 1)
            self.take_building_slot()
            if in_progress_building == NANITE_FACTORY:
                self.lock_shipyard()
                #TODO : add unlock to the event callback
            if in_progress_building == RESEARCH_LAB:
                self.empire.lock_research_lab()

        log.debug('Building levels of {} updated'.format(self.name))



    def update_planet_resources(self):
        menu.navigate_to_planet(self.name)
        # Force refresh of resources (after fleet deliveries)
        menu.navigate_to_overview()
        self.resources[METAL] = int(driver().find_element_by_id('resources_metal').get_attribute('innerHTML').replace('.', ''))
        self.resources[CRISTAL] = int(driver().find_element_by_id('resources_crystal').get_attribute('innerHTML').replace('.', ''))
        self.resources[DEUTERIUM] = int(driver().find_element_by_id('resources_deuterium').get_attribute('innerHTML').replace('.', ''))
        self.resources[ENERGY] = int(driver().find_element_by_id('resources_energy').get_attribute('innerHTML').replace('.', ''))
        # log.debug('Resource of {} updated'.format(self.name))

    def full_update(self):
        menu.navigate_to_planet(self.name)
        self.update_planet_resources()
        self.update_buildings_level()

    def get_building_level(self, building):
        return self._building_level[building]

    def set_building_level(self, building, level):
        self._building_level[building] = level

    def get_resource(self, resource_type):
        return self.resources[resource_type]

    def has_more_resources_than(self, cost):
        if METAL in cost and cost[METAL] > self.get_resource(METAL):
            return False
        if CRISTAL in cost and cost[CRISTAL] > self.get_resource(CRISTAL):
            return False
        if DEUTERIUM in cost and cost[DEUTERIUM] > self.get_resource(DEUTERIUM):
            return False
        return True

    def can_execute_task(self, task):
        log.debug('checking for execution of {}:\n{}'.format(task, task.__dict__))
        if get_type(task.object) == BUILDINGS:
            # Check special building nanite factory
            if task.object == NANITE_FACTORY:
                return self._shipyard_queue_empty and self._building_slot_available
            else:
                return self._building_slot_available
        if get_type(task.object) == SHIPYARD:
            # TODO:  make sure the shipyard queue cannot be full
            return not self._shipyard_locked # because of nanite
        log.error('Not implemented for this task : {}'.format(task))

    def lock_shipyard(self):
        self._shipyard_locked = True
    
    def unlock_shipyard(self):
        self._shipyard_locked = False

    def take_building_slot(self):
        self._building_slot_available = False

    def release_building_slot(self):
        self._building_slot_available = True

    # TODO: deal with shipyard
    def empty_shipyard_queue(self):
        self._shipyard_queue_empty = True

    def __str__(self):
        description = '{}\nResources : {}\nProduction : {}\n\nBuildings : {}'.format(self.name, self.resources, self.production, self._building_level)
        return description



class Empire():

    _tech_level = {
        ENERGY_TECH : 0,
        LASER_TECH : 0,
        ION_TECH : 0,
        PLASMA_TECH: 0,
        HYPERSPACE_TECH : 0,
        COMBUSTION_DRIVE : 0,
        PROPULSION_DRIVE : 0,
        HYPERSPACE_DRIVE : 0,
        ESPIONAGE_TECH : 0,
        COMPUTER_TECH : 0,
        ASTROPHYSICS_TECH : 0,
        INTERGALACTIC_RESEARCH_NETWORK :0,
        GRAVITON_TECH : 0,
        WEAPONS_TECH : 0,
        SHIELD_TECH : 0,
        ARMOR_TECH : 0,
    }

    _lab_lock = False

    
    def __init__(self):
        self.planets = {}
        self.generate_planets()
        self.update_research_level()

    def add_planet(self, planet):
        self.planets[planet.name] = planet
        planet.empire = self

    def generate_planets(self):
        planetNames = menu.list_planets()
        log.debug(str(planetNames))
        for planetName in planetNames:
            planet = Planet(planetName)
            self.add_planet(planet)

    def update_research_level(self):
        research_levels = extract_research_level()
        for tech in research_levels:
            self.set_research_level(tech, research_levels[tech])

        log.debug('Checking in progress research')

        in_progress_research = get_in_progress_research()
        if in_progress_research is not None:
            self.set_research_level(in_progress_research, self.get_research_level(in_progress_research) + 1)
            self.lock_research_lab()
        
        log.debug('Research levels updated')

    def get_research_level(self, tech_name):
        return self._tech_level[tech_name]

    def set_research_level(self, tech_name, level):
        self._tech_level[tech_name] = level

    def lock_research_lab(self):
        self._lab_lock = True

    def unlock_research_lab(self):
        self._lab_lock  = False

    def can_execute_task(self, task):
        if get_type(task.object) == RESEARCH:
            return  not self._lab_lock
        if get_type(task.object) == BUILDINGS:
            log.debug('checking for execution of building task {}:\n{}'.format(task, task.__dict__))
            # Check special building research lab
            if task.object == RESEARCH_LAB:
                return (not self._lab_lock) and self.planets[task.planet.name].can_execute_task(task)
            else:
                return self.planets[task.planet.name].can_execute_task(task)
        if get_type(task.object) == SHIPYARD:
            return self.planets[task.planet.name].can_execute_task(task)

    def __str__(self):
        description = str(self._tech_level) + '\n'
        description += ('\n\n' + 20 *'*' + '\n\n').join(map(str, self.planets.values()))
        return description




