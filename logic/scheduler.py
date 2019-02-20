import random
import logic.planet as planet
import navigation.research as research
import navigation.buildings as buildings
import navigation.shipyard as shipyard
import navigation.fleet as fleet
import time
from utils import *
from model.events import Event

random.seed()
currentTaskId = 0

log = get_module_logger(__name__)


def generateTaskId():
    global currentTaskId
    currentTaskId +=1
    return currentTaskId


class Goal():

    def __init__(self, object, planet, priority, level = -1, count=1):
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
        elif object in shipyard.deviceTranslation:
            return shipyard.SHIPYARD
        else:
            return None

    def is_building(self):
        return Goal.getType(self.object) == buildings.BUILDINGS

    def is_research(self):
        return Goal.getType(self.object) == research.RESEARCH

    def is_shipyard(self):
        return Goal.getType(self.object) == shipyard.SHIPYARD

    def level_to_build(self):
        if self.is_building():
            return (self.level - self.planet.get_building_level(self.object))
        if self.is_research():
            return (self.level - self.planet.empire.get_research_level(self.object))
        log.warn('Unhandled type for this goal ({} : {}), default to one level'.format(Goal.getType(self.object), self.object))
        return 1

    def generateTasks(self):
        #TODO: handle same element different levels with different priority
        n = 1
        if self.level > 0:
            n = self.level_to_build()

        resultingTasks = []
        dependency_id = None
        for i in range(n):
            priority = self.priority * math.pow(1.2, i)
            if dependency_id:
                newTask = Task(self.object, self.planet, priority, self.count, dependencies=[dependency_id])
            else:
                newTask = Task(self.object, self.planet, priority, self.count)

            dependency_id = newTask.id
            resultingTasks.append(newTask)

        # TODO: cascade requirement as new linked tasks
        log.debug('Goal {} translated in {} tasks'.format(str(self), len(resultingTasks)))
        return resultingTasks

    def __str__(self):
        description = 'Goal {} on {} with priority {}, level {}'.format(self.object, self.planet.name, self.priority, self.level)
        return description

class Task():

    def __init__(self, object, planet, priority, count, dependencies=None, preexecuteCall = None, postexecuteCall = None):
        self.object = object
        self.planet = planet
        self.priority = priority
        self.count = count
        self.cost = None
        self.id = generateTaskId()
        if dependencies is not None:
            self.dependencies = dependencies
        self.preexecuteCall = preexecuteCall
        self.postexecuteCall = postexecuteCall
    # TODO: add dependencies

    def execute(self):
        if self.preexecuteCall is not None:
            self.preexecuteCall()

        resultingEvent = None

        if Goal.getType(self.object) == buildings.BUILDINGS:
            log.debug('Bulding task : {}'.format(self.__str__()))
            resultingEvent = buildings.upgrade_building(self.planet.name, self.object)
        elif Goal.getType(self.object) == research.RESEARCH:
            log.debug('Researching task : {}'.format(self.__str__()))
            resultingEvent = research.researchTech(self.planet.name, self.object)
        else:
            log.warn('This type of task ({}) is not yet implemented'.format(Goal.getType(self.object)))
        #TODO:other cases (shipyard, fleet ...)

        resultingEvent.callback = self.postexecuteCall
        return resultingEvent

    def price(self):
        if Goal.getType(self.object) == buildings.BUILDINGS:
            self.cost = buildings.getBuildingCost(self.planet.name, self.object)
        elif Goal.getType(self.object) == research.RESEARCH:
            self.cost = research.getTechCost(self.planet.name, self.object)
        else:
            log.warn('This type of task pricing ({}) is not yet implemented'.format(Goal.getType(self.object)))
        #TODO:other cases (fleet ...)
    def isAffordable(self):
        self.planet.update_planet_resources()
        if self.cost is None:
            self.price()
        if METAL in self.cost and self.cost[METAL] > self.planet.get_resource(METAL):
            return False
        if CRISTAL in self.cost and self.cost[CRISTAL] > self.planet.get_resource(CRISTAL):
            return False
        if DEUTERIUM in self.cost and self.cost[DEUTERIUM] > self.planet.get_resource(DEUTERIUM):
            return False

        return True

    def __str__(self):
        description = 'Task {} : {} on {} with priority {}'.format(self.id, self.object, self.planet.name, self.priority)
        #TODO : add cost
        return description


class MasterScheduler():


    def __init__(self, configs):
        self.empire = planet.Empire()
        self.tasks = self.getStartingTasks(configs)
        self.events = self.seedEvents()
        log.debug(self.events)

    def lockResearchLab(self):
        #TODO
        pass
    def unlockResearchLab(self):
        #TODO
        pass
    #TODO lock/unlock shipyard

    def seedEvents(self):
        seeds = []
        for p in self.empire.planets:
            #Buildings
            seeds.append(Event(Event.BUILDING_IN_PROGRESS, buildings.getNextTimeAvailability(p) - time.time(), p))
            #Research
            seeds.append(Event(Event.RESEARCH_IN_PROGRESS, research.getNextTimeAvailability() - time.time(), p))
        #TODO: fleet movement
        #TODO: shipyard construction
        #TODO: periodic check

        return seeds


    def getStartingTasks(self, configs):
        goals = []
        for g in configs['goals']:
            count = 1
            level = -1
            if 'level' in g:
                level = g['level']
            if 'count' in g:
                count = g['count']
            goals.append(Goal(g['what'], self.empire.planets[g['planet']], g['priority'], level, count))

        tasks = []
        for goal in goals:
            tasks.extend(goal.generateTasks())
        return tasks


    def getNextEvent(self):
        self.events.sort(key= lambda x : x.getComplitionTime())
        log.debug('Current events in the queue :\n' + '\n'.join(map(str, self.events)))
        if len(self.events) == 0:
            log.warn('No more events to be treated')
            return False
        #Get next finishing event
        eventToLookAt = self.events.pop(0)
        log.info(eventToLookAt)
        if eventToLookAt.getComplitionTime() > time.time():
            # sleep until time to react to it
            log.info('sleeping for {} until event {} on {} finishes'
                     .format(seconds_to_formatted_time(eventToLookAt.getRemainingTime()),
                             eventToLookAt.type, eventToLookAt.planetName))
            time.sleep(eventToLookAt.getRemainingTime())
        #The event has finished, treat the consequences
        self.treatEvent(eventToLookAt)
        return True



    def treatEvent(self, event):
        log.info('Treating event : {}'.format(str(event)))
        if event.callback is not None:
            log.info('Event callback: {}'.format(event.callback))
            event.callback()
        if event.type == Event.BUILDING_IN_PROGRESS:
            #Building just finished, build next one
            taskToExecute = self.pickTask(event.planetName, buildings.BUILDINGS)
            if taskToExecute is not None:
                self.processTask(taskToExecute)
            else:
                #We do not build anything
                # to save money for some other task
                # or because we ran out of building task for this planet
                log.info('Not building anything this time on {}'.format(event.planetName))
        elif event.type == Event.RESEARCH_IN_PROGRESS:
            #Research is done, go to next one
            taskToExecute = self.pickTask(event.planetName, research.RESEARCH)
            if taskToExecute is not None:
                self.processTask(taskToExecute)
            else:
                # We do not research anything
                # to save money for some other task
                # or because we ran out of research task in the config file
                log.info('Not researching anything this time on {}'.format(event.planetName))
        elif event.type == Event.NO_MONEY:
            taskToExecute = self.pickTask(event.planetName)
            if taskToExecute is not None:
                self.processTask(taskToExecute)
            else:
                # We do not do anything
                log.info('Not doing anything this time on {}'.format(event.planetName))
        else:
            log.warn('Not yet implemented for {} event :\n{}'.format(event.type, event))

    def processTask(self, task):
        #TODO : remove affordability check when it is handled by the task picking
        if task.isAffordable():
            resultingEvent = task.execute()
            self.newEvent(resultingEvent)
            if resultingEvent.type != Event.ERROR:
                self.removeAchievedTask(task.id)
        else:
            # TODO: pick duration
            self.newEvent(Event(Event.NO_MONEY, random.gauss(5400, 600), task.planet.name))



    def pickTask(self, planetName, type=None):
        planet_tasks = self.filterTasksByPlanet(planetName)
        if len(planet_tasks) == 0:
            log.info('There are no task on this planet')
            return None

        log.debug('Tasks considered for planet {} :\n{}'.format(planetName, '\n'.join(map(str, planet_tasks))))

        top_priority_tasks = self.filter_top_priority_taks(planet_tasks)
        top_priority_affordable_tasks = self.filter_affordable_tasks(top_priority_tasks)
        top_priority_executable_tasks = self.filter_executable_tasks(top_priority_affordable_tasks)

        if top_priority_executable_tasks:
            # Execute a top priority task if possible
            log.debug('Top priority executable tasks considered for planet {} :\n{}'.format(planetName, '\n'.join(map(str, top_priority_executable_tasks))))
            return random.choice(top_priority_executable_tasks)
        else:
            # Find the highest priority tasks that can be executed
            top_priority = top_priority_tasks[0].priority
            highest_priority_tasks = self.filter_executable_tasks(self.filter_affordable_tasks(planet_tasks))
            if len(highest_priority_tasks) == 0:
                log.info('No executable task on planet {}'.format(planetName))
                return None
            best_alternative = random.choice(highest_priority_tasks)
            best_executable_priority = best_alternative.priority
            # Roll the dice and decide if the lower priority task is executed or if we wait to gather money/a slot for the top priority one
            alpha = 2
            # p probability of choosing the alternative
            p = math.exp(alpha * (best_executable_priority - top_priority) / top_priority)
            if random.random() < p:
                # Execute alternative
                log.debug('Executing alternative task with priority {} instead of top priority {} with a probability of {}'
                            .format(best_executable_priority, top_priority,  p))
                log.info('Task chosen for {} : {}'.format(planetName, str(best_alternative)))
                return best_alternative
            else:
                # Not executing anything and saving money / waiting for a top priority task to be executable
                log.debug('NOT executing alternative task with priority {} instead of top priority {} with a probability of {}'
                            .format(best_executable_priority, top_priority,  p))
                log.info('No task chosen for {}'.format(planetName))
                return None



    def newEvent(self, event):
        log.info('New event added : {}'.format(event))
        self.events.append(event)


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
        active = True
        while(active):
            active = self.getNextEvent()