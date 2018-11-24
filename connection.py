import time
import utils

driver = None
log = utils.get_module_logger(__name__)

#TODO: deal with loading problem and reload
def connect(config):
    #homepage
    driver.get(config['homeUrl'])
    #Open login menu
    driver.find_element_by_id('ui-id-1').click()

    time.sleep(1)
    #Removing ad
    try:
        cloaseAdZone = driver.find_element_by_class_name('openX_int_closeButton')
        closeAdButton = cloaseAdZone.find_element_by_tag_name('a')
        closeAdButton.click()
    except:
        pass
    # driver.find_element_by_id('loginBtn').click()
    #Fill credentials
    driver.find_element_by_id('usernameLogin').send_keys(config['email'])
    driver.find_element_by_id('passwordLogin').send_keys(config['password'])


    #Login
    driver.find_element_by_id('loginSubmit').click()

    log.info('Login submitted')

    # universeChoice = driver.find_element_by_id('serverLogin')
    # universeOptions = universeChoice.find_elements_by_tag_name("option")
    # for option in universeOptions:
    #     if config['universe'] in option.get_attribute('innerHTML') :
    #         option.click()

    time.sleep(3)

    actions = driver.find_elements_by_class_name('action-cell')
    for action in actions:
        if action.find_elements_by_tag_name('span')[0].get_attribute('innerHTML') == 'Play':
            action.click()
            log.info('Choosing the universe')
            return