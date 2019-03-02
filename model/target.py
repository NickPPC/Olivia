import time
import navigation.fleet as fleet


class Target():

    # TODO: honorable, bandit ...
    def __init__(self, galaxy, system, planet_id, rank, inactive):
        self._galaxy = galaxy
        self._system = system
        self._planet_id = planet_id
        self._rank = rank
        self._inactive = inactive
        self._creation_time = time.time()
        # Will be extracted from spy report
        self._spy_time = 0
        self._resources = {}
        self._fleet = {}
        self._defense = {}
        self._attack_bonus = 0
        self._shield_bonus = 0
        self._defense_bonus = 0

    def is_inactive(self):
        return self._inactive

    def get_rank(self):
        return self._rank

    def get_location_key(self):
        return '{}:{}:{}'.format(self._galaxy, self._system, self._planet_id)

    def spy(self, probes = 3):
        return fleet.spy(self._galaxy, self._system, self._planet_id, probes)

    def attack(self, fleet):
        return fleet.attack(self._galaxy, self._system, self._planet_id, fleet)

    def needed_fleet(self, max_fleet):
        #TODO
        pass


class SpyingReport():

    def __init__(self):
        # TODO: make configurable
        self._expires_at = time.time() + 1800