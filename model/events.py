from utils import get_module_logger, seconds_to_formatted_time
import time
from model.buildings import buildingTranslation, BUILDINGS
from model.research import researchTranslation, RESEARCH
from model.shipyard import deviceTranslation, SHIPYARD

log = get_module_logger(__name__)


class Event():

    BUILDING_IN_PROGRESS = 'Building in progress'
    RESEARCH_IN_PROGRESS = 'Research in progress'
    SHIPYARD_LOCKED = 'Shipyard is reserved for upgrade'
    RESEARCH_LAB_LOCKED = 'Research lab is reserved for upgrade'
    FLEET_ARRIVING = 'Fleet arriving'
    SPYING_IN_PROGRESS = 'Espionage probe(s) in flight'
    NO_MONEY = 'Not enough resources'
    NEED_ENERGY = 'Requires more energy'
    ERROR = 'Error !!'
    SHIPYARD_CONSTRUCTION_IN_PROGRESS = 'Shipard construction in progress'
    PERIODIC_CHECK = 'Periodic check'
    #TODO: create more event type (attacks, ...)


    def __init__(self, type, duration, planetName, description=''):
        log.debug('Event creation : {} , {}, {}, {}'.format(type, duration, planetName, description))
        self.type = type
        self.creationTime = time.time()
        # + 3 to make sure the pages have time to open and auto refresh
        self.duration = duration + 3
        self.description = description
        self.planetName = planetName
        self.callback = None

    def getComplitionTime(self):
        return self.creationTime + self.duration

    def getRemainingTime(self):
        return  self.duration - (time.time() - self.creationTime)


    def __str__(self):

        if self.getRemainingTime() > 0:
            finishTime = 'finishing in {}'.format(seconds_to_formatted_time(self.getRemainingTime()))
        else :
            finishTime = 'has ended'
        result = '{} started {} ago, {} on planet {}'\
            .format(self.type, seconds_to_formatted_time(time.time()- self.creationTime ),
                                finishTime, self.planetName)

        if self.description != '':
            result = '{} : {}'.format(result, self.description)

        return result

def get_type(object):
    if object in buildingTranslation:
        return BUILDINGS
    elif object in researchTranslation:
        return RESEARCH
    elif object in deviceTranslation:
        return SHIPYARD
    else:
        return None