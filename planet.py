import logging

from buildings import *
from research import extract_research_level
from research import ResearchScheduler
import menu
from utils import *
driver = None

log = get_module_logger(__name__)


class Planet():
    name = None
    #Resources
    resources = {
        METAL: 0,
        CRISTAL: 0,
        DEUTERIUM: 0,
        ENERGY: 0
    }
    #Production
    production = {
        METAL: 0,
        CRISTAL: 0,
        DEUTERIUM: 0,
        ENERGY: 0
    }
    # Buildings
    _building_level = {
        #Resources buildings
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

    def __init__(self, name, isResearchPlanet):
        self.name = name
        self.full_update()
        self.buildingScheduler = BuildingScheduler(name)
        if isResearchPlanet:
            self.researchScheduler = ResearchScheduler(name)

    def update_buildings_level(self):
        extract_resources_buildings_level(self)
        extract_facilities_buildings_level(self)


    def update_planet_resources(self):
        menu.navigate_to_planet(self.name)
        self.resources[METAL] = int(driver.find_element_by_id('resources_metal').get_attribute('innerHTML').replace('.', ''))
        self.resources[CRISTAL] = int(driver.find_element_by_id('resources_crystal').get_attribute('innerHTML').replace('.', ''))
        self.resources[DEUTERIUM] = int(driver.find_element_by_id('resources_deuterium').get_attribute('innerHTML').replace('.', ''))
        self.resources[ENERGY] = int(driver.find_element_by_id('resources_energy').get_attribute('innerHTML').replace('.', ''))

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

    def __str__(self):
        description = 'Resources : {}\nProduction : {}\n\nBuildings : {}'.format(self.resources, self.production, self._building_level)
        return description



class Empire():

    energyTech = 0
    laserTech = 0
    ionTech = 0
    plasmaTech = 0
    hyperspaceTech = 0
    combustionDrive = 0
    propulsionDrive = 0
    hyperspaceDrive = 0
    espionageTech = 0
    computerTech = 0
    astrophysicsTech = 0
    intergalacticResearchNetwork = 0
    gravitonTech = 0
    weaponsTech = 0
    shieldTech = 0
    armorTech = 0

    
    def __init__(self, researchPlanet=None):
        self.planets = {}
        self.generate_planets(researchPlanet)
        self.update_research_level()

    def add_planet(self, planet):
        self.planets[planet.name] = planet

    def generate_planets(self, researchPlanet):
        planetNames = menu.list_planets()
        for planetName in planetNames:
            doesResearch = False
            if researchPlanet is not None and planetName == researchPlanet:
                doesResearch = True
            planet = Planet(planetName, doesResearch)
            self.add_planet(planet)

    def update_research_level(self):
        extract_research_level(self)


    def __str__(self):
        description = ('\n\n' + 20 *'*' + '\n\n').join(map(str, self.planets.values()))
        return description




