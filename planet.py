from agent import driver
from buildings import extract_resources_buildings_level, extract_facilities_buildings_level

class Planet():
    name = None
    #Resources
    metal = 0
    cristal = 0
    deuterium = 0
    #Production
    metalProd = 0
    cristalProd = 0
    deuteriumProd = 0
    #Resources buildings
    metalMineLevel = 0
    cristalMineLevel = 0
    deuteriumMineLevel = 0
    solarPlantLevel = 0
    fissionPlantLevel = 0
    metalSiloLevel = 0
    cristalSiloLevel = 0
    deuteriumSiloLevel = 0
    #Facilities buildings
    roboticsFactory = 0
    shipyard = 0
    researchLab = 0
    allianceDepot = 0
    missileSilo = 0
    naniteFactory = 0
    terraformer = 0
    spaceDock = 0

    def __init__(self, name):
        self.name = name
        self.update_planet_resources()
        self.update_buildings_level()

    def update_buildings_level(self):
        extract_resources_buildings_level(self)
        extract_facilities_buildings_level(self)


    def update_planet_resources(self):
        self.metal = driver.find_element_by_id('resources_metal').get_attribute('innerHTML')
        self.cristal = driver.find_element_by_id('resources_crystal').get_attribute('innerHTML')
        self.deuterium = driver.find_element_by_id('resources_deuterium').get_attribute('innerHTML')

    def description(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())



class Empire():
    
    def __init__(self):
        self.planets = {}

    def add_planet(self, planet):
        self.planets[planet.name] = planet

    def description(self):
        description = ""
        for p in self.planets:
            description += "{} : {}".format(p, self.planets[p].description())
        return description


def generate_planet(empire):
    #TODO extract planets' name
    planet = Planet('HomeWorld')
    empire.add_planet(planet)

