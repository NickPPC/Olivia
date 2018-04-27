import math
import logging
import json



METAL = 'metal'
CRISTAL = 'cristal'
DEUTERIUM = 'deuterium'

def get_module_logger(mod_name):
  logger = logging.getLogger(mod_name)
  handler = logging.StreamHandler()
  formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s - %(funcName)20s %(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG)
  return logger

log = get_module_logger(__name__)


def seconds_to_formatted_time(seconds):
    # log.debug('seconds = {}'.format(seconds))
    timeLeft = int(math.ceil(seconds))
    s = timeLeft % 60
    timeLeft = int((timeLeft - s)/60)
    m = timeLeft % 60
    timeLeft = int((timeLeft - m)/60)
    h = timeLeft % 24
    timeLeft = int((timeLeft - h) /24)
    d = timeLeft

    formattedTime = ''
    if d != 0:
        formattedTime += '{} d'.format(d)
    if h != 0:
        formattedTime += ' {} h'.format(h)
    if m != 0:
        formattedTime += ' {} m'.format(m)
    if s != 0:
        formattedTime += ' {} s'.format(s)

    # log.debug('format = {}'.format(formattedTime))


    return formattedTime

def formatted_time_to_seconds(formattedTime):
    # log.debug('format = {}'.format(formattedTime))

    # Parsing
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    if 'd' in formattedTime:
        days = int(formattedTime.split('d')[0])
        formattedTime = formattedTime.split('d')[1]
    if 'h' in formattedTime:
        hours = int(formattedTime.split('h')[0])
        formattedTime = formattedTime.split('h')[1]
    if 'm' in formattedTime:
        minutes = int(formattedTime.split('m')[0])
        formattedTime = formattedTime.split('m')[1]
    if 's' in formattedTime:
        seconds = int(formattedTime.split('s')[0])

    timeInSeconds = ((days * 24 + hours) * 60 + minutes) * 60 + seconds
    # log.debug('seconds = {}'.format(timeInSeconds))

    return timeInSeconds



def cost_extraction(costListElement):
    cost = {METAL: 0, CRISTAL: 0, DEUTERIUM: 0}
    try:
        cost[METAL] = int(costListElement.find_element_by_class_name('metal').find_element_by_class_name('cost').get_attribute(
            'innerHTML').replace('.', ''))
    except:
        pass
    try:
        cost[CRISTAL] = int(costListElement.find_element_by_class_name('crystal').find_element_by_class_name('cost').get_attribute(
            'innerHTML').replace('.', ''))
    except:
        pass
    try:
        cost[DEUTERIUM] = int(costListElement.find_element_by_class_name('deuterium').find_element_by_class_name(
            'cost').get_attribute('innerHTML').replace('.', ''))
    except:
        pass

    return cost

def level_extraction(levelElementText):

    while '<' in levelElementText:
        i = levelElementText.find('<')
        j = levelElementText.find('>')
        if i == 0:
            levelElementText = levelElementText[j + 1:]
            levelElementText = levelElementText[levelElementText.find('>') + 1:]
        else:
            levelElementText = levelElementText[:i - 1]
            levelElementText.strip()
    return int(levelElementText)