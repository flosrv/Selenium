from imports import *
from constants import *

def back_to_home(driver):
    driver.get(website_url)
    print("Retour à la page d'accueil...")

def create_driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)
    driver.maximize_window()
    driver.get(website_url)

    # Scroll jusqu'en bas de la page
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time_sleep()
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Revenir en haut
    driver.execute_script("window.scrollTo(0, 0);")

    return driver

def time_sleep():
    time.sleep(random.uniform(1,3))

def find_child_elements(element):
    children = element.find_elements(By.XPATH,"*/.." )
    return children

def find_parent_element(element):
    children = element.find_element(By.XPATH,"./.." )
    return children

def get_all_attributes(element, driver):
    return driver.execute_script("""
        let elem = arguments[0];
        let attrs = {}; 
        for (let attr of elem.attributes) { 
            attrs[attr.name] = attr.value 
        } 
        return attrs;
    """, element)


def click_with_JS(element, driver):
    driver.execute_script("arguments[0].click();", element)


def find_element(driver, criteria, element):
    criteria = criteria.strip().lower()
    
    by_map = {
        'id': By.ID,
        'name': By.NAME,
        'xpath': By.XPATH,
        'css': By.CSS_SELECTOR,
        'class': By.CLASS_NAME,
        'tag': By.TAG_NAME,
        'link': By.LINK_TEXT,
        'partial_link': By.PARTIAL_LINK_TEXT
    }

    if criteria not in by_map:
        raise ValueError(f"[find_element] Critère non reconnu : '{criteria}'")

    return driver.find_element(by_map[criteria], element)



def find_elements(driver, criteria, element):
    criteria = criteria.strip().lower()
    
    by_map = {
        'id': By.ID,
        'name': By.NAME,
        'xpath': By.XPATH,
        'css': By.CSS_SELECTOR,
        'class': By.CLASS_NAME,
        'tag': By.TAG_NAME,
        'link': By.LINK_TEXT,
        'partial_link': By.PARTIAL_LINK_TEXT
    }

    if criteria not in by_map:
        raise ValueError(f"[find_elements] Critère non reconnu : '{criteria}'")

    return driver.find_elements(by_map[criteria], element)









