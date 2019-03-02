import time
import utils
from utils import get_driver as driver

log = utils.get_module_logger(__name__)

def connect(config):
    #homepage
    driver().get(config['homeUrl'])
    #Open login menu
    driver().find_element_by_id('ui-id-1').click()

    time.sleep(1)

    utils.remove_ad()

    #Fill credentials
    driver().find_element_by_id('usernameLogin').send_keys(config['email'])
    driver().find_element_by_id('passwordLogin').send_keys(config['password'])


    #Login
    driver().find_element_by_id('loginSubmit').click()

    log.debug('Login submitted')

    # universeChoice = driver().find_element_by_id('serverLogin')
    # universeOptions = universeChoice.find_elements_by_tag_name("option")
    # for option in universeOptions:
    #     if config['universe'] in option.get_attribute('innerHTML') :
    #         option.click()

    time.sleep(3)

    try:
        joinGame = driver().find_element_by_id('joinGame')
        if joinGame is not None:
            play_button = joinGame.find_element_by_tag_name('a').find_element_by_tag_name('button')

            play_button.click()

        time.sleep(3)
    except Exception as e:
        log.error(e)

    actions = driver().find_elements_by_class_name('action-cell')
    for action in actions:
        # TODO find better distinction
        if action.find_elements_by_tag_name('span')[0].get_attribute('innerHTML') == 'Play' or \
            action.find_elements_by_tag_name('span')[0].get_attribute('innerHTML') == 'Jouer':
            action.click()
            log.info('Choosing the universe')
            break

        time.sleep(5)
    # Closing first tab
    del driver().window_handles[0]
    driver().switch_to.window(driver().window_handles[0])
    time.sleep(1)
    driver().close()
    time.sleep(2)
    # Focusing on open tab
    driver().switch_to.window(driver().window_handles[0])