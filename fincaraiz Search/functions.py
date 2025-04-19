from imports import *
from constants import *

def choose_rent_buy_projects(driver, choice):
    try:
        # On récupère les labels cliquables
        radio_buttons = driver.find_elements(By.CSS_SELECTOR, ".ant-radio-button-wrapper")

        for button in radio_buttons:
            # On extrait le texte dans le span de texte
            text = button.find_elements(By.TAG_NAME, "span")[-1].text.strip()

            print(f"Option trouvée : {text}")

            if text.lower() == choice.lower():
                button.click()
                print(f">> '{text}' sélectionné.")
                break

    except Exception as e:
        print(f"Erreur : {str(e)}")

def remove_unwanted_elements(driver, selectors, timeout=3):
    """
    Supprime de la page tous les éléments correspondant aux sélecteurs donnés avec un délai global pour tout.
    
    :param driver: L'instance du WebDriver
    :param selectors: Une liste de sélecteurs CSS correspondant aux éléments à supprimer
    :param timeout: Le délai global d'attente (en secondes) pour tous les éléments
    """
    try:
        # Attendre que tous les éléments soient présents dans le délai global
        WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ', '.join(selectors)))
        )

        # Recherche et suppression de chaque élément via Selenium
        for selector in selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                for element in elements:
                    driver.execute_script("arguments[0].remove();", element)  # Suppression de l'élément via JavaScript
                print(f"Éléments supprimés avec le sélecteur : {selector}")
            else:
                print(f"Aucun élément trouvé pour le sélecteur : {selector}")

    except TimeoutException:
        # Si aucun des éléments n'a été trouvé dans le délai global
        print(f"Aucun élément trouvé pour les sélecteurs dans le délai global de {timeout} secondes.")
    except Exception as e:
        print(f"Erreur lors de la suppression des éléments : {e}")

def login(driver, email, password):
    # Cliquer sur le bouton de login
    try:
        driver.get(website_url)
        nuke_fincaraiz_cookie_popup(driver)
      
        time.sleep(3)

        # Attendre que le bouton devienne cliquable (jusqu'à 10 secondes)
        login_button = WebDriverWait(driver=driver, timeout=3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-secondary"))
        )

        login_button.click()
        print("Clicked on Ingresar...")

        time.sleep(1.5)
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(email)
        print("Filled email field...")
        email_field.send_keys(Keys.ENTER)
        time.sleep(1)

        contrasena_field = driver.find_element(By.ID, "password")
        contrasena_field.send_keys(password)
        contrasena_field.send_keys(Keys.ENTER)
        remove_unwanted_elements(driver, unwanted_selectors)
        username = driver.find_element(By.XPATH, "//span[@class='username']")
        if username:
            print("Connexion réussie!")
            
    except Exception as e:
        print(f"Erreur lors de la connexion :\n{e}")

def fermer_fenetre_modal(driver, timeout=5):
    try:
        # Attendre que le bouton de fermeture soit cliquable
        close_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close-button"))
        )
        close_button.click()
        print("✅ Modale fermée avec succès.")
    except Exception as e:
        print(f"❌ Impossible de fermer la modale :\n{e}")

def nuke_fincaraiz_cookie_popup(driver, timeout=5, retry_interval=0.5):
    """Supprime le pop-up cookie de Fincaraiz en cliquant sur 'Accept all' ou via JS fallback."""

    print("⏳ Tentative de suppression du popup Fincaraiz...")
    end_time = time.time() + timeout
    popup_gone = False

    while time.time() < end_time:
        try:
            # Tentative de clic sur le bouton 'Accept all' si présent
            buttons = driver.find_elements(By.CSS_SELECTOR, ".fc-button-label")
            for btn in buttons:
                if "accept all" in btn.text.lower():
                    try:
                        btn.click()
                        print("✅ Bouton 'Accept all' cliqué.")
                        popup_gone = True
                        break
                    except (ElementClickInterceptedException, Exception) as e:
                        print(f"⚠️ Erreur lors du clic sur le bouton 'Accept all' : {e}")
            
            if popup_gone:
                break

            # Fallback JS si le bouton n'est pas interactable ou pas encore là
            driver.execute_script("""
                const popup = document.querySelector('.fc-dialog-scrollable-content');
                if (popup) popup.remove();

                const overlay = document.querySelector('.fc-consent-root');
                if (overlay) overlay.remove();

                document.body.style.overflow = 'auto';
            """)
            still_there = driver.execute_script("""
                return document.querySelector('.fc-dialog-scrollable-content') !== null ||
                       document.querySelector('.fc-consent-root') !== null;
            """)
            if not still_there:
                popup_gone = True
                break

        except JavascriptException as e:
            print(f"⚠️ Erreur JS : {e}")

        time.sleep(retry_interval)

    if popup_gone:
        print("🧨 Pop-up Fincaraiz supprimé.")
    else:
        print("❌ Pop-up non supprimé après le délai imparti.")

def clear_ant_select_choices(driver):
    try:
        # Cliquer sur le champ pour forcer l'ouverture du dropdown
        select_area = driver.find_element(By.CSS_SELECTOR, ".ant-select-selector")
        select_area.click()
        time.sleep(0.5)  # laisser le temps à l'UI

        # Ensuite, supprimer les éléments sélectionnés
        remove_buttons = driver.find_elements(By.CSS_SELECTOR, ".ant-select-selection-item-remove")
        for btn in remove_buttons:
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.2)

        print("✅ Sélections supprimées.")
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage des sélections : {e}")

def back_to_home(driver):
    # set url to https://www.fincaraiz.com.co/
    driver.get(website_url)
    print("Retour à la page d'accueil...")

def create_driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2) 
    return driver

def search(driver, list_real_estate_type, location):
    try:
        back_to_home(driver)
        nuke_fincaraiz_cookie_popup(driver)
        clear_ant_select_choices(driver)

        type_mapping = {
            "apartamento": "Apartamento",
            "casa": "Casa",
            "apartaestudio": "Apartaestudio",
            "cabana": "Cabaña",
            "casa campestre": "Casa Campestre",
            "lote": "Casa Lote",
            "finca": "Finca",
            "habitacion": "Habitación"
        }

        if list_real_estate_type:
            dropdown_real_estate_type = driver.find_element(By.CSS_SELECTOR, ".ant-select-selector")
            dropdown_real_estate_type.click()
            time.sleep(1)

            for item in list_real_estate_type:
                item_lower = item.lower()
                if item_lower in type_mapping:
                    try:
                        option_title = type_mapping[item_lower]
                        option = driver.find_element(By.CSS_SELECTOR, 
                            f"div[title='{option_title}'] div[class='ant-select-item-option-content']")
                        option.click()
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"Erreur lors du clic sur l'option '{option_title}': {e}")
                else:
                    print(f"Type '{item}' non reconnu.")

        if location:
            ubicacion_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='🔍︎ Busca por ubicación']")
            ubicacion_input.clear()
            ubicacion_input.send_keys(location)
            ubicacion_input.send_keys(Keys.ENTER)
            time.sleep(1)
            print("Recherche en cours...")

        fermer_fenetre_modal(driver)

        search_button = driver.find_element(By.CSS_SELECTOR, "button.search-button")
        search_button.click()

    except Exception as e:
        print(f"Erreur lors de la recherche :\n{e}")

def select_real_estate_types(driver, real_estate_types):
    try:
        # Ouvrir le dropdown
        driver.find_element(By.CSS_SELECTOR, ".ant-select-selector").click()

        # Attendre que toutes les options soient visibles
        options = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ant-select-item-option"))
        )

        # On désélectionne uniquement ce qui est sélectionné mais qu'on ne veut pas
        for opt in options:
            text = opt.text.strip().lower()
            is_selected = "ant-select-item-option-selected" in opt.get_attribute("class")
            should_be_selected = any(q.lower() in text for q in real_estate_types)

            if is_selected and not should_be_selected:
                driver.execute_script("arguments[0].click();", opt)
                print(f"❌ Désélectionné : {opt.text.strip()}")

        # Ensuite on sélectionne ce qu'on veut, seulement si pas déjà sélectionné
        for opt in options:
            text = opt.text.strip().lower()
            is_selected = "ant-select-item-option-selected" in opt.get_attribute("class")

            for query in real_estate_types:
                if query.lower() in text and not is_selected:
                    driver.execute_script("arguments[0].click();", opt)
                    print(f"✅ Sélectionné : {opt.text.strip()}")
                    break

        # Vérif finale : on ajuste au cas où
        for opt in options:
            text = opt.text.strip().lower()
            is_selected = "ant-select-item-option-selected" in opt.get_attribute("class")
            should_be_selected = any(q.lower() in text for q in real_estate_types)

            if is_selected and not should_be_selected:
                driver.execute_script("arguments[0].click();", opt)
                print(f"❌ Corrigé (désélection) : {opt.text.strip()}")
            elif not is_selected and should_be_selected:
                driver.execute_script("arguments[0].click();", opt)
                print(f"✅ Corrigé (sélection) : {opt.text.strip()}")

        print("🎯 Sélection vérifiée et corrigée.")

    except Exception as e:
        print(f"💥 Erreur : {str(e)}")





































