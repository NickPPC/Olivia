from navigation.fleet import get_fleet_numbers, spy
from navigation.galaxy import crawl_galaxy
from utils import get_module_logger
import navigation.menu as menu
import time
import random


log = get_module_logger(__name__)

MAX_RANK = 'max_rank'
SEARCH_DISTANCE = 'search_distance'

class SpyingReport():

    def __init__(self):
        # TODO: make configurable
        self._expires_at = time.time() + 1800

class FleetManager():

    _targets = []

    def __init__(self, fleet_config):
        (current, max_fleet) = get_fleet_numbers()
        self._max_fleet = max_fleet
        self._available_fleet_slots = max_fleet - current
        log.info('{} fleet slots available out of {}'.format(self._available_fleet_slots, self._max_fleet))
        self._max_target_rank = fleet_config[MAX_RANK]
        self._search_distance = fleet_config[SEARCH_DISTANCE]
        self.search_for_targets(self._search_distance, self._max_target_rank)

    def search_for_targets(self, distance, max_rank):
        log.info('Search area : {} systems'.format(distance))
        planets = crawl_galaxy(distance)
        log.info('{} planets in the search area'.format(len(planets)))
        # Filtering for inactive
        inactive_targets = [p for p in planets if p[2]]
        log.info('{} inactive targets in the search area'.format(len(inactive_targets)))
        # Filtering out low ranking players
        self._targets = [p for p in inactive_targets if p[1] > max_rank]
        log.info('{} inactive targets with a ranking higher than {} in this serach area'.format(len(self._targets), max_rank))
        log.debug('\n'.join(map(str, self._targets)))

    def pick_next_target(self):
        #TODO
        return random.choice(self._targets)

    def test_spy(self):
        menu.navigate_to_planet('Phoenix')
        while self._available_fleet_slots > 0:
            target_address = self.pick_next_target()[0]
            spy(target_address.split(':')[0], target_address.split(':')[1], target_address.split(':')[2], 1)
            self._available_fleet_slots -= 1


    

        


