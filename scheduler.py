import logging
import random
import planet
import research
import buildings
import fleet
import time
import menu
from utils import *

random.seed()
currentTaskId = 0

log = get_module_logger(__name__)


def generateTaskId():
    global currentTaskId
    currentTaskId +=1
    return currentTaskId

class Event():

    BUILDING_IN_PROGRESS = 'Building in progress'
    RESEARCH_IN_PROGRESS = 'Research in progress'
    FLEET_ARRIVING = 'Fleet arriving'
    NO_MONEY = 'Not enough resources'
    ERROR = 'Error !!'
    #TODO: create more event type (attacks, ...)

    def __init__(self, type, duration, planetName, description=''):
        log.debug('Event creation : {} , {}, {}, {}'.format(type, duration, planetName, description))
        self.type = type
        self.creationTime = time.time()
        self.duration = duration + 3
        self.description = description
        self.planetName = planetName

    def getComplitionTime(self):
        return self.creationTime + self.duration

    def getRemainingTime(self):
        return  self.duration - (time.time() - self.creationTime)


    def __str__(self):
        result = '{} started {} ago, finishing in {} on planet {}'\
            .format(self.type, seconds_to_formatted_time(time.time()- self.creationTime ),
                                                seconds_to_formatted_time(self.getRemainingTime()), self.planetName)

        if self.description != '':
            result = '{} : {}'.format(result, self.description)

        return result

class Goal():

    def __init__(self, object, level, planet, priority, count=1):
        self.object = object
        self.level = level
        self.planet = planet
        self.priority = priority
        self.count = count

    @staticmethod
    def getType(object):
        if object in buildings.buildingTranslation:
            return buildings.BUILDINGS
        elif object in research.researchTranslation:
            return research.RESEARCH
        #TODO: fleet/defense

    def generateTasks(self):

        # TODO: cascade requirement as new linked tasks
        resultingTasks = [Task(self.object, self.planet, self.priority, self.count)]
        log.debug('Goal {} translated in {} tasks'.format(str(self), len(resultingTasks)))
        return resultingTasks

class Task():

    def __init__(self, object, planet, priority, count):
        self.object = object
        self.planet = planet
        self.priority = priority
        self.count = count
        self.cost = None
        self.id = generateTaskId()
    # TODO: add dependencies

    def execute(self):
        menu.navigate_to_planet(self.planet.name)
        if Goal.getType(self.object) == buildings.BUILDINGS:
            log.debug('Bulding task : {}'.format(str(self)))
            return self.planet.buildingScheduler.upgrade_building(self.object)
        else:
            log.warn('This type of task ({}) is not yet implemented'.format(Goal.getType(self.object)))
        #TODO:other cases (research, fleet ...)

    def price(self):
        menu.navigate_to_planet(self.planet.name)
        if Goal.getType(self.object) == buildings.BUILDINGS:
            self.cost = self.planet.buildingScheduler.getBuildingCost(self.object)
        else:
            log.warn('This type of task privcing ({}) is not yet implemented'.format(Goal.getType(self.object)))
        #TODO:other cases (research, fleet ...)
    def isAffordable(self):
        self.planet.update_planet_resources()
        if METAL in self.cost and self.cost[METAL] > self.planet.metal:
            return False
        if CRISTAL in self.cost and self.cost[CRISTAL] > self.planet.cristal:
            return False
        if DEUTERIUM in self.cost and self.cost[DEUTERIUM] > self.planet.deuterium:
            return False

        return True

    def __str__(self):
        description = 'Task {} : {} on {} with priority {}'.format(self.id, self.object, self.planet.name, self.priority)
        #TODO : add cost
        return description


class MasterScheduler():


    def __init__(self, configs):
        self.empire = planet.Empire()
        self.researchPlanet = configs[research.RESEARCH_PLANET]
        self.tasks = self.getTasks(configs)
        self.events = self.seedEvents()
        log.debug(self.events)

    def seedEvents(self):
        seeds = []
        #Buildings
        for p in self.empire.planets:
            seeds.append(Event(Event.BUILDING_IN_PROGRESS, self.empire.planets[p].buildingScheduler.nextTimeAvailable - time.time(), p))
        #Research
        # seeds.append(Event(Event.RESEARCH_IN_PROGRESS,
        #                    self.empire.planets[self.researchPlanet].researchScheduler.nextTimeAvailable - time.time(),
        #                    self.researchPlanet))
        #TODO: fleet movement
        #TODO: shipyard construction
        #TODO: periodic check

        return seeds


    def getTasks(self, configs):
        goals = []
        for g in configs['goals']:
            count = 1
            if 'count' in g:
                count = g['count']
            goals.append(Goal(g['what'], g['level'], self.empire.planets[g['planet']], g['priority'], count))

        tasks = []
        for goal in goals:
            tasks.extend(goal.generateTasks())
        return tasks


    def getNextEvent(self):
        self.events.sort(key= lambda x : x.getComplitionTime())
        log.debug('Current events in the queue : ' + '; '.join(map(str, self.events)))
        #Get next finishing event
        eventToLookAt = self.events.pop(0)
        log.info(eventToLookAt)
        if eventToLookAt.getComplitionTime() > time.time():
            # sleep until time to react to it
            log.info('sleeping for {} until next event {}'
                     .format(seconds_to_formatted_time(eventToLookAt.getRemainingTime()), str(eventToLookAt)))
            time.sleep(eventToLookAt.getRemainingTime())
        #The event has finished, treat the consequences
        self.treatEvent(eventToLookAt)



    def treatEvent(self, event):
        log.info('Treating event : {}'.format(str(event)))
        if event.type == Event.BUILDING_IN_PROGRESS:
            #Building just finished, build next one
            taskToExecute = self.pickTask(event.planetName)
            if taskToExecute is not None:
                taskToExecute.price()
                if taskToExecute.isAffordable():
                    if (self.newEvent(taskToExecute.execute())):
                        self.removeAchievedTask(taskToExecute.id)
                else:
                    #TODO: pick duration
                    self.newEvent(Event(Event.NO_MONEY, random.gauss(5400, 600), event.planetName))
            else:
                #We do not build anything
                # to save money for some other task
                # or because we ran out of building task for this planet
                log.info('Not building anything this time on {}'.format(event.planetName))
                # TODO: add a check status event ?
        elif event.type == Event.NO_MONEY:
            taskToExecute = self.pickTask(event.planetName)
            taskToExecute.price()
            if taskToExecute.isAffordable():
                self.newEvent(taskToExecute.execute())
            else:
                log.debug('Still cannot afford')
                # TODO: pick duration
                self.newEvent(Event(Event.NO_MONEY, random.gauss(5400, 600), event.planetName))
            self.removeAchievedTask(taskToExecute.id)

    #TODO
    def pickTask(self, planetName):
        relevantTasks = self.filterTasksByPlanet(planetName)
        log.debug('Tasks considered for planet {} : {}'.format(planetName, '; '.join(map(str, relevantTasks))))
        # TODO: arbitration algorithm based on priority
        if len(relevantTasks) > 0:
            taskToExecute = relevantTasks.pop(0)
            log.info('Task chosen for {} : {}'.format(planetName, str(taskToExecute)))
            return taskToExecute
        else:
            log.info('No task chosen for {}'.format(planetName))
            return None


    def newEvent(self, event):
        log.info('New event added : {}'.format(event))
        self.events.append(event)
        if event.type == Event.ERROR:
            return False
        else:
            return True

    def removeAchievedTask(self, taskId):
        index = None
        for i in range(len(self.tasks)):
            if self.tasks[i].id == taskId:
                index = i
        if index == None:
            log.error('Impossible to removing task {}'.format(taskId))
        else:
            self.tasks.pop(index)

    def filterTasksByPlanet(self, planetName):
        return sorted(
            [t for t in self.tasks if t.planet.name == planetName],
            key=lambda x: x.priority, reverse=True)

    def filterTasks(self, planetName, type):
        return sorted(
            [t for t in self.tasks if t.planet.name == planetName and Goal.getType(t.object) == type],
            key=lambda x : x.priority, reverse=True)

    def run(self):

        while(True):
            self.getNextEvent()