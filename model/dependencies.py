from model.buildings import *
from model.research import *
from model.shipyard import *


dependencies = {
    # Tech
    ENERGY_TECH : [(RESEARCH_LAB, 1)],
    LASER_TECH : [(ENERGY_TECH, 2)],
    ION_TECH : [(ENERGY_TECH, 4), (LASER_TECH, 5), (RESEARCH_LAB, 4)],
    PLASMA_TECH: [(ENERGY_TECH, 8), (LASER_TECH, 10), (ION_TECH, 5)],
    COMBUSTION_DRIVE : [(ENERGY_TECH, 1)],
    PROPULSION_DRIVE : [(ENERGY_TECH, 1), (RESEARCH_LAB, 2)],
    HYPERSPACE_TECH : [(SHIELD_TECH, 5), (ENERGY_TECH, 5), (RESEARCH_LAB, 7)],
    HYPERSPACE_DRIVE : [(HYPERSPACE_TECH, 3)],
    ESPIONAGE_TECH : [(RESEARCH_LAB, 3)],
    COMPUTER_TECH : [(RESEARCH_LAB, 1)],
    WEAPONS_TECH : [(RESEARCH_LAB, 4)],
    SHIELD_TECH : [(RESEARCH_LAB, 6), (ENERGY_TECH, 3)],
    ARMOR_TECH : [(RESEARCH_LAB, 2)],
    INTERGALACTIC_RESEARCH_NETWORK : [(HYPERSPACE_TECH, 8), (RESEARCH_LAB, 10), (COMPUTER_TECH, 8)],
    ASTROPHYSICS_TECH : [(RESEARCH_LAB, 3), (ESPIONAGE_TECH, 4), (PROPULSION_DRIVE, 3)],
    GRAVITON_TECH : [(RESEARCH_LAB, 12)],

    # Buildings
    FISSION_PLANT : [(DEUTERIUM_MINE, 5), (ENERGY_TECH, 3)],
    SHIPYARD : [(ROBOTICS_FACTORY, 2)],
    NANITE_FACTORY : [(COMPUTER_TECH, 10), (ROBOTICS_FACTORY, 10)],
    TERRAFORMER : [(NANITE_FACTORY, 1), (ENERGY_TECH, 12)],
    SPACE_DOCK : [(SHIPYARD, 1)],

    # Spacecrafts
    #TODO

    # Defense
    PLASMA_CANON : [(PLASMA_TECH, 7), (SHIPYARD, 8)]
    # TODO




}