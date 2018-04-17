import time



def connect(driver, config):
    #homepage
    driver.get(config['homeUrl'])
    #Open login menu

    time.sleep(1)
    #Removing ad
    cloaseAdZone = driver.find_element_by_class_name('openX_int_closeButton')
    closeAdButton = cloaseAdZone.find_element_by_tag_name('a')
    closeAdButton.click()
    driver.find_element_by_id('loginBtn').click()
    #Fill credentials
    driver.find_element_by_id('usernameLogin').send_keys(config['email'])
    driver.find_element_by_id('passwordLogin').send_keys(config['password'])
    universeChoice = driver.find_element_by_id('serverLogin')
    universeOptions = universeChoice.find_elements_by_tag_name("option")
    for option in universeOptions:
        if config['universe'] in option.get_attribute('innerHTML') :
            option.click()

    #Login
    driver.find_element_by_id('loginSubmit').click()
