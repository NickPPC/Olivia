import planet
import research
import buildings
import fleet


#TODO


class MasterScheduler():


    def __init__(self, configFile):
        self.empire = planet.Empire()
        self.buildingSchedulers = self.init_building_schedulers(configFile)
        self.researchScheduler = self.init_research_scheduler(configFile)
        self.fleetScheduler = self.init_fleet_scheduler(configFile)
        self.events = []

    def init_building_schedulers(self, configFile):
        #TODO: read goals from config
        schedulers = [buildings.BuildingScheduler(planet, []) for planet in self.empire.planets.values()]
        return schedulers

    def init_research_scheduler(self, configFile):
        #TODO: read goals from config
        researchPlanet = self.empire.planets['HomeWorld']
        return research.ResearchScheduler(researchPlanet, [])

    def init_fleet_scheduler(self, configFile):
        #TODO: read goals from config
        return fleet.FleetScheduler([])