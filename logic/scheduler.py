import random
import logic.planet as planet
import navigation.research as research
import navigation.buildings as buildings
import navigation.shipyard as shipyard
import navigation.fleet as fleet
import time
from utils import *
from model.events import Event, get_type
from logic.fleet import FleetManager
from model.dependencies import dependencies

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

    def is_building(self):
        return get_type(self.object) == buildings.BUILDINGS

    def is_research(self):
        return get_type(self.object) == research.RESEARCH

    def is_shipyard(self):
        return get_type(self.object) == shipyard.SHIPYARD

    def count_to_build(self):
        if get_type(self.object) == shipyard.SHIPYARD:
            #TODO deal with ships
            return self.count - self.planet.get_defense_count(self.object)
        
        return self.count


    def level_to_build(self, already_planned_tasks):
        already_planned = 0
        for planned_task in already_planned_tasks:
            if planned_task.object == self.object:
                already_planned += 1

        if self.is_building():
            return (self.level - self.planet.get_building_level(self.object) - already_planned)
        if self.is_research():
            return (self.level - self.planet.empire.get_research_level(self.object) - already_planned)
        log.warn('Unhandled type for this goal ({} : {}), default to one level'.format(get_type(self.object), self.object))
        return 1

    def generate_tasks(self, already_planned_tasks):

        count = self.count_to_build()
        if count <= 0:
            # Nothing to do
            return []

        n = 1
        if self.level > 0:
            n = self.level_to_build(already_planned_tasks)

        resultingTasks = []
        dependency_id = None
        for i in range(n):
            priority = self.priority * math.pow(1.2, n - i - 1)
            
            if dependency_id:
                newTask = Task(self.object, self.planet, priority, count, dependencies=[dependency_id])
            else:
                newTask = Task(self.object, self.planet, priority, count)

            dependency_id = newTask.id
            resultingTasks.append(newTask)

        prerequisite_tasks = self.generate_prerequisite(already_planned_tasks)

        for prereq in prerequisite_tasks:
            for task in resultingTasks:
                task.dependencies.append(prereq.id)
        
        resultingTasks.extend(prerequisite_tasks)

        log.debug('Goal {} translated in {} tasks'.format(str(self), len(resultingTasks)))
        return resultingTasks

    def generate_prerequisite(self, already_planned_tasks):
        if self.object not in dependencies:
            log.debug('No depencies for {}'.format(self.object))
            return []

        prereqs = []
        for dep in dependencies[self.object]:
            # Check if prerquisite filled
            dep_goal = Goal(dep[0], self.planet, self.priority, dep[1])
            if dep[0] == buildings.RESEARCH_LAB or dep[0] in research.researchTranslation:
                # For techs and research lab move requirement on planet with best lab
                dep_goal.planet = self.planet.empire.get_best_research_planet()
            dep_tasks = dep_goal.generate_tasks(already_planned_tasks)
            prereqs.extend(dep_tasks)
            already_planned_tasks.extend(dep_tasks)

        return prereqs

    @staticmethod
    def translate_goals(goals):
        # TODO
        # TODO: handle same element different levels with different priority

        tasks = []
        for g in goals:
            tasks.extend(g.generate_tasks(list(tasks)))
        return tasks

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
        else:
            self.dependencies = []
        self.preexecuteCall = preexecuteCall
        self.postexecuteCall = postexecuteCall
    # TODO: add dependencies

    def execute(self):
        if self.preexecuteCall is not None:
            self.preexecuteCall()

        resultingEvent = None

        if get_type(self.object) == buildings.BUILDINGS:
            log.debug('Bulding task : {}'.format(self.__str__()))
            resultingEvent = buildings.upgrade_building(self.planet.name, self.object)
        elif get_type(self.object) == research.RESEARCH:
            log.debug('Researching task : {}'.format(self.__str__()))
            resultingEvent = research.researchTech(self.planet.name, self.object)
        elif get_type(self.object) == shipyard.SHIPYARD:
            log.debug('Shipyard task : {} {} on {}'.format(self.count, self.object, self.planet.name))
            resultingEvent = shipyard.build_device(self.planet.name, self.object, self.count)
        else:
            log.warn('This type of task ({}) is not yet implemented'.format(get_type(self.object)))
        #TODO:other cases (fleet ...)

        resultingEvent.callback = self.postexecuteCall
        return resultingEvent

    def price(self):
        log.debug('Pricing {}'.format(self.__str__()))
        if get_type(self.object) == buildings.BUILDINGS:
            self.cost = buildings.getBuildingCost(self.planet.name, self.object)
        elif get_type(self.object) == research.RESEARCH:
            self.cost = research.getTechCost(self.planet.name, self.object)
        elif get_type(self.object) == shipyard.SHIPYARD:
            self.cost = shipyard.getDeviceCost(self.object, self.count)
        else:
            log.warn('This type of task pricing ({}) is not yet implemented'.format(get_type(self.object)))

    def isAffordable(self):
        self.planet.update_planet_resources()
        if self.cost is None:
            self.price()
        return self.planet.has_more_resources_than(self.cost)

    def affordability_not_changed_by(self, other_task):
        # Should not be necessary but just in case
        if self.cost is None:
            self.price()
        if other_task.cost is None:
            other_task.price()
        
        combined_cost = dict(self.cost)
        for resource in other_task.cost:
            if resource in combined_cost:
                combined_cost[resource] + other_task.cost[resource]
            else:
                combined_cost[resource] = other_task.cost[resource]
            if not self.planet.has_more_resources_than({resource: combined_cost[resource]}) and \
                other_task.cost[resource] > 0:
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
        log.debug('Events:\n' + '\n'.join(map(str, self.events)))
        log.debug('Tasks:\n' + '\n'.join(map(str, self.tasks)))
        self.fleet_manager = FleetManager(configs['fleet'])
        # self.fleet_manager.test_spy()

    #TODO lock/unlock shipyard

    def seedEvents(self):
        seeds = []
        for p in self.empire.planets:
            #Buildings
            next_availability = buildings.getNextTimeAvailability(p) - time.time()
            if next_availability > 0:
                self.empire.planets[p].take_building_slot()
                seeds.append(Event(Event.BUILDING_IN_PROGRESS, next_availability, p))

            #Research
            if self.empire.planets[p].get_building_level(buildings.RESEARCH_LAB) > 0:
                next_availability = research.getNextTimeAvailability() - time.time()
                if next_availability > 0:
                    seeds.append(Event(Event.RESEARCH_IN_PROGRESS, next_availability, p))
                    self.empire.lock_research_lab()

            # First event to trigger potential construction
            seeds.append(Event(Event.INITIAL_CHECK, 0, p))

            # # Shipyard
            # if self.empire.planets[p].get_building_level(buildings.SHIPYARD) > 0:
            #     #TODO : extract when queue empty
            #     seeds.append(Event(Event.SHIPYARD_CONSTRUCTION_IN_PROGRESS, 0, p))

        #TODO: fleet movement
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

        return Goal.translate_goals(goals)


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
            #Building just finished, allow a new one to be built
            self.empire.planets[event.planetName].release_building_slot()
        elif event.type == Event.RESEARCH_IN_PROGRESS:
            #Research is done, allow a new one to be started or the researvch lab to be upgraded
            self.empire.unlock_research_lab()
        elif event.type == Event.PERIODIC_CHECK:
            pass
        elif event.type == Event.SHIPYARD_CONSTRUCTION_IN_PROGRESS:
            # TODO : update shipyard queue
            pass
        else:
            log.warn('Not yet implemented for {} event :\n{}'.format(event.type, event))

        task_to_execute = self.pickTask(event.planetName)
        while task_to_execute is not None:
            self.processTask(task_to_execute)
            task_to_execute = self.pickTask(event.planetName)

        # If there is nothing else to do stop now, otherwise add periodic check
        if len(self.get_planet_tasks(event.planetName)) > 0:
            # If not doing anything create a periodic check to trigger construction
            self.newEvent(Event(Event.PERIODIC_CHECK, 3 * 3600, event.planetName))
            log.info('Not doing anything at this time on {}'.format(event.planetName))


    def processTask(self, task):

        resultingEvent = task.execute()
        self.newEvent(resultingEvent)
        if resultingEvent.type != Event.ERROR:
            resultingEvent.callback = lambda : self.remove_achieved_task(task.id)
            self.remove_launched_task(task.id)

            if get_type(task.object) == buildings.BUILDINGS:
                self.empire.planets[task.planet.name].take_building_slot()
                if task.object == buildings.RESEARCH_LAB:
                    self.empire.lock_research_lab()
                if task.object == buildings.NANITE_FACTORY or task.object == buildings.SHIPYARD:
                    self.empire.planets[task.planet.name].lock_shipyard()
            if get_type(task.object) == research.RESEARCH:
                self.empire.lock_research_lab()
            if get_type(task.object) == shipyard.SHIPYARD:
                # Extend the shipyard is done event
                #TODO
                pass


    def pickTask(self, planetName):
        planet_tasks = self.get_planet_tasks(planetName)
        if len(planet_tasks) == 0:
            log.warn('There are no task on this planet')
            return None

        log.debug('Tasks considered for planet {} :\n{}'.format(planetName, '\n'.join(map(str, planet_tasks))))

        top_priority_tasks = self.filter_top_priority_tasks(planet_tasks)
        log.debug('Top priority tasks on planet {} : {}'.format(planetName, '\n'.join(map(str, top_priority_tasks))))
        top_priority_available_tasks = self.filter_executable_tasks(top_priority_tasks)
        log.debug('Possible top priority tasks on planet {} : {}'.format(planetName, '\n'.join(map(str, top_priority_available_tasks))))
        top_priority_executable_tasks = self.filter_affordable_tasks(top_priority_available_tasks)
        log.debug('Top priority executable and affordable tasks on planet {} : {}'.format(planetName, '\n'.join(map(str, top_priority_executable_tasks))))

        if len(top_priority_executable_tasks) > 0:
            # Execute a top priority task if possible
            log.debug('Top priority executable tasks considered for planet {} :\n{}'.format(planetName, '\n'.join(map(str, top_priority_executable_tasks))))
            return random.choice(top_priority_executable_tasks)
        else:
            # Find the highest priority tasks that can be executed
            top_priority = top_priority_tasks[0].priority
            highest_priority_executable_tasks = self.filter_top_priority_tasks(self.filter_affordable_tasks(self.filter_executable_tasks(planet_tasks)))
            log.debug('Highest priority executable and  affordable tasks on planet {} : {}'.format(planetName, '\n'.join(map(str, highest_priority_executable_tasks))))

            if len(highest_priority_executable_tasks) == 0:
                log.info('No executable task on planet {}'.format(planetName))
                return None
            # Checking if there is a task that will not change the affordability ot top priority tasks
            non_impacting_tasks = []
            executable_tasks = self.filter_affordable_tasks(self.filter_executable_tasks(planet_tasks))
            for t in executable_tasks:
                has_no_impact = True
                for top_priority_task in top_priority_tasks:
                    has_no_impact = has_no_impact and top_priority_task.affordability_not_changed_by(t)
                if has_no_impact:
                    non_impacting_tasks.append(t)
            log.debug('Executable money non impacting tasks on planet {} : {}'.format(planetName, '\n'.join(map(str, non_impacting_tasks))))

            if len(non_impacting_tasks) > 0:
                # Pick one of those tasks regardless of priority differential
                non_impacting_chosen_task = random.choice(self.filter_top_priority_tasks(non_impacting_tasks))
                log.info('Picking task which does not impact affordability of top priority task : {}'.format(non_impacting_chosen_task))
                return non_impacting_chosen_task
            else:
                log.debug('No money non impacting task found')
            best_alternative = random.choice(highest_priority_executable_tasks)
            best_executable_priority = best_alternative.priority
            # Roll the dice and decide if the lower priority task is executed or if we wait to gather money/a slot for the top priority one
            alpha = 0.5
            # p probability of choosing the alternative
            p = math.exp(alpha * float(best_executable_priority - top_priority) / float(best_executable_priority))
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


    def remove_launched_task(self, taskId):
        index = None
        for i in range(len(self.tasks)):
            if self.tasks[i].id == taskId:
                index = i
        if index == None:
            log.error('Impossible to removing task {}'.format(taskId))
        else:
            self.tasks.pop(index)

    def remove_achieved_task(self, task_id):
        # Remove dependencies
        for t in self.tasks:
            if task_id in t.dependencies:
                t.dependencies.remove(task_id)


    def get_planet_tasks(self, planetName):
        return sorted(
            [t for t in self.tasks if (t.planet.name == planetName and len(t.dependencies) == 0)],
            key=lambda x: x.priority, reverse=True)

    # def filter_tasks_by_type(self, planetName, type):
    #     return sorted(
    #         [t for t in self.tasks if t.planet.name == planetName and get_type(t.object) == type],
    #         key=lambda x : x.priority, reverse=True)

    def filter_top_priority_tasks(self, tasks):
        sorted_tasks = sorted(tasks, key= lambda x: x.priority, reverse=True)
        if len(sorted_tasks) == 0:
            return []
        top_priority = sorted_tasks[0].priority
        return [t for t in sorted_tasks if t.priority == top_priority]

    def filter_affordable_tasks(self, tasks):
        return [t for t in tasks if t.isAffordable()]

    def filter_executable_tasks(self, tasks):
        return [t for t in tasks if self.empire.can_execute_task(t)]


    def run(self):
        active = True
        while(active):
            active = self.getNextEvent()
        log.warn('Stopping scheduler')