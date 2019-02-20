
SHIPYARD = 'shipyard'
DEFENSE = 'defense'
#Military ships
LIGHT_FIGHTER = 'lightFighter'
HEAVY_FIGHTER = 'heavyFighter'
CRUISER = 'cruiser'
BATTLESHIP = 'battleship'
BATTLECRUISER = 'battlecruiser'
BOMBER = 'bomber'
DESTROYER = 'destroyer'
DEATHSTAR = 'deathStar'
#Civilian ships
SMALL_TRANSPORTER = 'smallTransporter'
LARGE_TRANSPORTER = 'largeTransporter'
RECYCLER = 'recycler'
SPY_PROBE = 'spyProbe'
COLONY_SHIP = 'colonyShip'
SOLAR_SATELLITE = 'solarSatellite'
#Defense
MISSILE_LAUCHER = 'missileLauncher'
LIGHT_LASER_DEFENSE = 'lightLaserDefense'
HEAVY_LASER_DEFENSE = 'heavyLaserDefense'
ION_CANON = 'ionCanon'
GAUSS_CANON = 'gaussCanon'
PLASMA_CANON = 'plasmaCanon'
SMALL_SHIELD = 'smallShield'
LARGE_SHIELD = 'largeShield'
DEFENSE_MISSILE = 'interceptionMissile'
ATTACK_MISSILE = 'interplanetarMissile'

deviceTranslation = {
    #Shipyard
    LIGHT_FIGHTER : (SHIPYARD, 'details204'),
    HEAVY_FIGHTER : (SHIPYARD, 'details205'),
    CRUISER: (SHIPYARD, 'details206'),
    BATTLESHIP: (SHIPYARD, 'details207'),
    BATTLECRUISER: (SHIPYARD, 'details215'),
    BOMBER: (SHIPYARD, 'details211'),
    DESTROYER: (SHIPYARD, 'details213'),
    DEATHSTAR: (SHIPYARD, 'details214'),
    SMALL_TRANSPORTER: (SHIPYARD, 'details202'),
    LARGE_TRANSPORTER: (SHIPYARD, 'details203'),
    COLONY_SHIP: (SHIPYARD, 'details208'),
    RECYCLER: (SHIPYARD, 'details209'),
    SPY_PROBE: (SHIPYARD, 'details210'),
    SOLAR_SATELLITE: (SHIPYARD, 'details212'),
    #Defense
    MISSILE_LAUCHER : (DEFENSE, 'details401'),
    LIGHT_LASER_DEFENSE: (DEFENSE, 'details402'),
    HEAVY_LASER_DEFENSE: (DEFENSE, 'details403'),
    ION_CANON: (DEFENSE, 'details404'),
    GAUSS_CANON: (DEFENSE, 'details405'),
    PLASMA_CANON: (DEFENSE, 'details406'),
    SMALL_SHIELD: (DEFENSE, 'details407'),
    LARGE_SHIELD: (DEFENSE, 'details408'),
    DEFENSE_MISSILE: (DEFENSE, 'details502'),
    ATTACK_MISSILE: (DEFENSE, 'details503'),
}

deviceCost = {
    #Shipyard
    LIGHT_FIGHTER : (3000, 1000, 0),
    HEAVY_FIGHTER : (6000, 4000, 0),
    CRUISER: (20000, 7000, 2000),
    BATTLESHIP: (45000, 15000, 0),
    BATTLECRUISER: (30000, 40000, 15000),
    BOMBER: (50000, 25000, 15000),
    DESTROYER: (60000, 50000, 15000),
    DEATHSTAR: (5000000, 4000000, 1000000),
    SMALL_TRANSPORTER: (2000, 2000, 0),
    LARGE_TRANSPORTER: (6000, 6000, 0),
    COLONY_SHIP: (10000, 20000, 10000),
    RECYCLER: (10000, 6000, 2000),
    SPY_PROBE: (0, 1000, 0),
    SOLAR_SATELLITE: (0, 2000, 500),
    #Defense
    MISSILE_LAUCHER : (2000, 0, 0),
    LIGHT_LASER_DEFENSE: (1500, 500, 0),
    HEAVY_LASER_DEFENSE: (6000, 2000, 0),
    ION_CANON: (2000, 6000, 0),
    GAUSS_CANON: (20000, 15000, 2000),
    PLASMA_CANON: (50000, 50000, 30000),
    SMALL_SHIELD: (10000, 10000, 0),
    LARGE_SHIELD: (50000, 50000, 0),
    DEFENSE_MISSILE: (8000, 2000, 0),
    ATTACK_MISSILE: (12500, 2500, 10000),
}