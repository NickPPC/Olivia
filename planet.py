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
    #TODO

    def __init__(self, name):
        self.name = name

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


def generate_planet(driver, empire):
    #TODO extract planets' name
    planet = Planet('HomeWorld')
    update_planet_resources(driver, planet)
    # print(planet.description())
    empire.add_planet(planet)

def update_planet_resources(driver, planet):
    planet.metal = driver.find_element_by_id('resources_metal').get_attribute('innerHTML')
    planet.cristal = driver.find_element_by_id('resources_crystal').get_attribute('innerHTML')
    planet.deuterium = driver.find_element_by_id('resources_deuterium').get_attribute('innerHTML')
