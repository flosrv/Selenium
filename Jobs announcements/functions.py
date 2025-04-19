from imports import *
from constants import *

def close_banner(driver, timeout=3):
    try:
        # 1. Attente du popup par ID
        popup = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, 
                            "pop-up-webpush-sub"))
        )
        close_button = WebDriverWait(popup, timeout).until(
            EC.element_to_be_clickable((By.XPATH, ".//button[2]"))
        )
        close_button.click()
        time.sleep(1)

    except (TimeoutException, NoSuchElementException):
        # Popup non trouvé ou non cliquable, fallback JS
        try:
            driver.execute_script("""
                const el = document.getElementById("pop-up-webpush-sub");
                if (el) {
                    el.style.display = 'none';
                    el.remove();
                }
            """)
            time.sleep(1)
        except Exception:
            pass  # Ignore l'échec JS

    # 2. Suppression générique d'overlay (au cas où)
    try:
        driver.execute_script("""
            let overlay = document.querySelector('.overlay');
            if (overlay) {
                overlay.style.display = 'none';
                overlay.remove();
            }
        """)
        time.sleep(1)
    except Exception:
        pass

    # 3. Scroll pour forcer le DOM à se mettre à jour (optionnel)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

def close_overlay(driver, timeout=3):
    try:
        # Vérifier l'existence de l'overlay dans un délai de 5 secondes
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.overlay, #pop-up-webpush-background'))
        )
        # 1. Supprimer tous les overlays en JS
        driver.execute_script("""
            const overlays = document.querySelectorAll('.overlay, #pop-up-webpush-background');
            overlays.forEach(overlay => {
                overlay.style.display = 'none';  // Masquer l'overlay
                overlay.remove();  // Supprimer complètement l'élément du DOM
            });
        """)
        time.sleep(1)  # Temps pour vérifier que l'overlay a disparu
        print("Overlay supprimé avec succès")
    except Exception as e:
        print(f"Aucun overlay trouvé ou erreur lors de la suppression : {e}")

def search_for_jobs(driver, keywords, location=None):
    driver.get(website_path)
    close_banner(driver)
    job_field = driver.find_element(By.XPATH, "//input[@id='prof-cat-search-input']")
    job_field.clear()  
    job_field.send_keys(keywords)
    
    time.sleep(1)

    if location is not None:
        location_bar = driver.find_element(By.XPATH, "//input[@id='place-search-input']")
        location_bar.clear()  
        location_bar.send_keys(location)
        location_bar.send_keys(Keys.ENTER)
        close_banner(driver)

    search_button = driver.find_element(By.XPATH, "//button[@id='search-button']")
    search_button.click()
    close_banner(driver)
    close_overlay(driver)
    
def create_driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2) 
    return driver

def login(driver, email, password):
    # Cliquer sur le bouton de login
    try:
        driver.get(website_path)
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
        
        try:
            info_users = driver.find_element(By.CSS_SELECTOR, "div[class='info_user'] span")
            info_users.click()
            print("Clicked on User infos !")
        except Exception as e:
            print('Element not found')

    except Exception as e:
       print(f"Erreur lors de la connexion :\n{e}")

def go_to_next_page_with_siguiente(driver):
    try:
        # Attendre que le bouton "Siguiente" soit visible et cliquable
        siguiente = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[@title='Siguiente']"))
        )
        
        # Si le bouton "Siguiente" est affiché et cliquable
        if siguiente.is_displayed() and siguiente.is_enabled():
            print("Bouton 'Siguiente' trouvé, clic sur le bouton")
            siguiente.click()
            close_banner(driver)
            close_overlay(driver)
            return True
        else:
            print("Bouton 'Siguiente' non cliquable ou absent")
            return False

    except Exception as e:
        return False

def find_offers_div(driver):
        # Cherche le conteneur principal des offres
        offers_container = driver.find_element(By.ID, "offersGridOfferContainer")
        if offers_container:
            # Cherche tous les articles dont l'ID commence par quelque chose (à préciser si besoin)
            offers = offers_container.find_elements(By.XPATH, ".//article[starts-with(@id, '')]")
            
            if offers:
                print(f"{len(offers)} offres trouvées.")
                return offers
            else:
                print("Aucune offre trouvée dans le conteneur.")
        else:
            print("Conteneur 'offersGridOfferContainer' introuvable.")
































