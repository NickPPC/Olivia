from buildings import extract_facilities_buildings_level, extract_resources_buildings_level
from research import extract_research_level
driver = None

class Planet():
    name = None
    #Resources
    metal = 0
    cristal = 0
    deuterium = 0
    energy = 0
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
        self.energy = driver.find_element_by_id('resources_energy').get_attribute('innerHTML')


    def __str__(self):
        attrs = vars(self)
        return '\n'.join("%s: %s" % item for item in attrs.items())



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

    
    def __init__(self):
        self.planets = {}
        self.generate_planet()
        self.update_research_level()
        #TODO: initialize with all planets

    def add_planet(self, planet):
        self.planets[planet.name] = planet

    def generate_planet(self):
        # TODO extract planets' name
        planet = Planet('HomeWorld')
        self.add_planet(planet)

    def update_research_level(self):
        extract_research_level(self)


    def __str__(self):
        description = ('\n' + 20 *'*' + '\n').join(map(str, self.planets.values()))
        return description




