from imports import *
from constants import *

# Fonction pour récupérer le code de vérification depuis l'email


def back_to_home(driver):
    driver.get(website_url)
    print("Retour à la page d'accueil...")

def create_driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2) 
    driver.maximize_window()  # Maximiser la fenêtre
    return driver


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













