from imports import *
from constants import *





def tuer_popup_fincaraiz(driver):
    try:
        print("Attente de la popup de consentement...")
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fc-dialog-container"))
        )
        print("Popup détectée. Tentative de suppression...")
        driver.execute_script("""
            let popup = document.querySelector('.fc-dialog-container');
            if (popup) {
                popup.remove();
                console.log('Popup supprimée à coups de JavaScript !');
            }
        """)
        print("Popup supprimée avec succès.")
    except TimeoutException:
        print("Pas de popup détectée dans les 3 secondes.")

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


def remove_popups_and_overlay(driver):
    try:
        # Exécuter du JavaScript pour supprimer l'overlay et la popup de consentement
        driver.execute_script("""
            var overlay = document.querySelector(".fc-dialog-overlay");
            if (overlay) {
                overlay.parentNode.removeChild(overlay);
                console.log("Overlay supprimé avec succès.");
            }

            var consentPopup = document.querySelector(".fc-consent-root");
            if (consentPopup) {
                consentPopup.parentNode.removeChild(consentPopup);
                console.log("Popup de consentement supprimée avec succès.");
            }
        """)
    except Exception as e:
        print(f"Erreur lors de la suppression des popups et de l'overlay : {e}")

def login(driver, email, password):
    try:
        driver.get(website_url)
        remove_popups_and_overlay(driver)
        time.sleep(3)

        # Attente que le bouton devienne cliquable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-secondary"))
        )

        # Forcer le clic sur le bouton en utilisant JavaScript si nécessaire
        driver.execute_script("arguments[0].click();", login_button)

        print("Clicked on Ingresar...")

        time.sleep(1.5)

        # Remplir les champs de connexion
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(email)
        email_field.send_keys(Keys.ENTER)
        time.sleep(1)

        contrasena_field = driver.find_element(By.ID, "password")
        contrasena_field.send_keys(password)
        contrasena_field.send_keys(Keys.ENTER)
        
        # Supprimer les éléments indésirables
        remove_popups_and_overlay(driver)
        
        # Vérifier si l'utilisateur est connecté
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

def choisir_type_annonce(buy_rent_projects_chosen, driver):
    wait = WebDriverWait(driver, 4)
    try:
        home_container = wait.until(
            EC.presence_of_element_located((By.ID, "home-container"))
        )

        targets = ["Arriendo", "Proyectos", "Venta"]

        elements = home_container.find_elements(By.XPATH, ".//*")

        for el in elements:
            try:
                text = el.text.strip()
                if el.tag_name.lower() == "label" and text in targets:
                    if buy_rent_projects_chosen.lower() in text.lower() :
                        el.click()
                        print(f"🖱️ Cliqué sur '{text}'")
                        break
            except Exception as e:
                print(f"[!] Erreur sur un élément : {e}")

    except Exception as e:
        print(f"[❌] Erreur globale : {e}")

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


def parse_typology(raw_text):
    import re
    match = re.search(r"(\d+)\s+Habs?.\s+(\d+)\s+Baño.*?([\d,.]+)\s*m²", raw_text)
    if match:
        return {
            "rooms": int(match.group(1)),
            "bathrooms": int(match.group(2)),
            "area_m2": float(match.group(3).replace(",", "."))
        }
    return {}


def extract_card_info(card_element):
    try:
        title = card_element.find_element(By.CSS_SELECTOR, "a.lc-cardCover").get_attribute("title")
        href = card_element.find_element(By.CSS_SELECTOR, "a.lc-cardCover").get_attribute("href")
        
        img = card_element.find_element(By.CLASS_NAME, "card-image-gallery--img").get_attribute("src")
        price = card_element.find_element(By.CLASS_NAME, "price").text
        typology = card_element.find_element(By.CLASS_NAME, "lc-typologyTag").text
        location = card_element.find_element(By.CLASS_NAME, "lc-location").text
        
        # Extraction du projet et du constructeur avec vérification de la présence d'éléments
        publisher_elements = card_element.find_elements(By.CSS_SELECTOR, ".publisher strong")
        
        project_name = publisher_elements[0].text if len(publisher_elements) > 0 else ""
        constructor = publisher_elements[1].text if len(publisher_elements) > 1 else ""
        
        # Nettoyage de la typologie (chambres, salle de bain, surface)
        typology_details = parse_typology(typology)
        
        return {
            "title": title,
            "image": img,
            "price": price,
            "typology": typology_details,
            "location": location,
            "project": project_name,
            "constructor": constructor
        }
    except Exception as e:
        print(f"Erreur lors de l'extraction: {str(e)}")
        return None


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



















