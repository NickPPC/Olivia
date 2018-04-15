import menu

def go_to_resources(driver):
    menu.navigate_to_tab(driver, 'resources')

def extract_resources_buildings_level(driver, planet):
    buildingsList = driver.find_element_by_id('building')
    planet.metalMineLevel = int(buildingsList.find_element_by_class_name('supply1')\
        .find_element_by_class_name('level').get_attribute('innerHTML').split('>')[2].strip())
    planet.cristalMineLevel = int(buildingsList.find_element_by_class_name('supply2') \
        .find_element_by_class_name('level').get_attribute('innerHTML').split('>')[2].strip())
    planet.deuteriumMineLevel = int(buildingsList.find_element_by_class_name('supply3') \
        .find_element_by_class_name('level').get_attribute('innerHTML').split('>')[2].strip())
    #TODO:finish