from imports import *
from functions import *

driver = create_driver()
driver.get(website_url)
wait = WebDriverWait(driver, timeout=3)
mi_cuenta = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Mi cuenta']")))  # Remplacer par l'élément attendu
mi_cuenta.click()
# Envoie de l'email sur le site
try:
    ingresar_email_zone = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Ingresa tu email']")))
    ingresar_email_zone.clear()
    ingresar_email_zone.send_keys(EMAIL)
    ingresar_email_zone.send_keys(Keys.ENTER)
except:
    print('NO')



