from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time,json, dataclasses
from typing import List, Optional


Dataclass = dataclasses.dataclass

@Dataclass
class Offer:
    title: str
    company: Optional[str] = None
    verified : bool = False
    location : str
    contract_type: str
    schedule: str
    location: str
    salary: Optional[int] = None


creds_path = r"C:\Users\f.gionnane\Documents\Selenium\Jobs announcements\connection_creds.json"
with open(creds_path, 'r') as file:
    content = json.load(file)
    email = content['email']
    password = content['password']

# URL du site
website_path = "https://co.computrabajo.com/"

# Creation du driver Chrome avec ses options et headers


def create_driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2) 
    driver.get(website_path)
    return driver
driver = create_driver()

time.sleep(3)  # Laisse le temps à la page de charger



def login(driver, email, password):
    # Cliquer sur le bouton de login
    try:
        time.sleep(3)
    
        login_button = driver.find_element(By.XPATH, "//span[@class='b_primary_inv']")
        login_button.click()
        time.sleep(1)
        ingresar_button = driver.find_element(By.XPATH, "//span[@alt='Ingresar']")
        ingresar_button.click()
        time.sleep(1.5)
        email_field = driver.find_element(By.XPATH, "//input[@id='LoginModel_Email']")
        email_field.send_keys(email)
        
        continuar_button = driver.find_element(By.XPATH, "//a[@id='continueWithMailButton']")
        continuar_button.click()
        time.sleep(1)
        contrasena_field = driver.find_element(By.XPATH, "//input[@id='LoginModel_Password']")
        contrasena_field.send_keys(password)
        contrasena_field.send_keys(Keys.ENTER)
        img_head_cv = driver.find_element(By.XPATH, "//img[@name='imgheadcv']")
        if img_head_cv:
            print("Connexion réussie!")
    except Exception as e:
        print(f"Erreur lors de la connexion :\n{e}")

login(driver, email, password)

def search_for_jobs(driver, keywords, location):
    job_field = driver.find_element(By.XPATH, "//input[@id='prof-cat-search-input']")
    
    job_field.send_keys(keywords)
    job_field.send_keys(Keys.ENTER)
    time.sleep(1)

    location_bar = driver.find_element(By.XPATH, "//input[@id='place-search-input']")
    location_bar.send_keys(location)
    location_bar.send_keys(Keys.ENTER)
    time.sleep(1)
    try:
        ahora_no_button = "//button[@onclick='webpush_subscribe_ko(event);']"
        if driver.find_element_by_xpath(ahora_no_button):
            ahora_no_button = driver.find_element_by_xpath(ahora_no_button)
            ahora_no_button.click()
            time.sleep(1)
    except:
        pass

search_for_jobs(driver, "Científico de Datos", "Barranquilla")

def collect_offers(driver):
    offers = []

    try:
        jobs_div = driver.find_elements(By.XPATH,"//article[@class='box_offer']")
        for job in jobs_div:
            job.click()
            time.sleep(1)
            details = driver.find_element(By.XPATH, "//div[@class='box_detail']").text

            job_title = details.find_element(By.XPATH, "//p[@class='title_offer']").text
            company_name = details.find_element(By.XPATH, "//p[@class='company_offer']").text

    except Exception as e:
        print(f"Erreur lors de la récupération des détails :\n{e}")