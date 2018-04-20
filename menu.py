driver = None
def navigate_to_tab(tabName):
    tab = None
    menu = driver.find_element_by_id('menuTable')

    for element in menu.find_elements_by_tag_name('a'):
        try:
            if tabName in element.get_attribute('href'):
                tab = element
        except:
            pass

    tab.click()

def navigate_to_overview():
    navigate_to_tab('overview')