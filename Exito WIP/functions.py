from imports import *
from constants import *



def back_to_home(driver):
    driver.get(website_url)
    print("Retour à la page d'accueil...")

def create_driver():
    
    # Initialisation des options pour le driver
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)
    driver.maximize_window()
    
    # Ouverture de la page web
    driver.get(website_url)

    # Scroll jusqu'en bas de la page
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Ajout d'un délai pour laisser la page se charger
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Revenir en haut
    driver.execute_script("window.scrollTo(0, 0);")
    
    return driver

def time_sleep():
    time.sleep(random.uniform(1,3))

def time_sleep(page=1, action="default", page_type="listing"):
    """
    Attente réaliste en fonction de l'action, du type de page et de la progression.

    Args:
        page (int): Numéro de la page actuelle.
        action (str): Type d'action : 'click', 'scroll', 'navigate', 'default'
        page_type (str): Type de page : 'listing', 'product'
    """
    
    # Base time ranges selon action
    action_base_times = {
        "click": (1.5, 2.5),
        "scroll": (0.8, 1.5),
        "navigate": (2.5, 3.5),
        "default": (2, 3)
    }

    # Ajustement si c’est une fiche produit (on lit +)
    product_multiplier = 1.4 if page_type == "product" else 1.0

    # Progression légère (fatigue)
    fatigue_factor = 0.05 * page  # +0.05s par page

    # Choix du temps de base selon action
    base_min, base_max = action_base_times.get(action, (2, 3))
    base_time = uniform(base_min, base_max)

    # Calcul final
    wait_time = base_time * product_multiplier + fatigue_factor

    # Pause longue tous les 7 pages
    if page % 7 == 0:
        long_pause = randint(5, 10)  # pause entre 5 et 10s
        print(f"😴 Pause longue (page {page}) : {long_pause} sec")
        sleep(long_pause)
    else:
        sleep(wait_time)

def filter_products_img_urls(img_urls):
    """
    Filtre une liste d'URLs d'images pour ne garder que celles qui contiennent **tous** les termes définis dans 'list_accepted_terms'.
    """
    list_accepted_terms = ["vtexassets", "arquivos", "ids", "v="]
    
    # Filtrer et garder uniquement les URLs qui contiennent **tous** les termes nécessaires
    filtered_urls = [url for url in img_urls if all(term in url for term in list_accepted_terms)]
    
    return filtered_urls

def normalize_text(text):
    # Supprimer les sauts de ligne et les espaces inutiles
    text = text.replace("\n", " ")  # Remplacer les sauts de ligne par un espace
    text = re.sub(r'\s+', ' ', text)  # Remplacer les espaces multiples par un seul espace
    text = text.strip()  # Supprimer les espaces en début et fin de texte
    return text

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
    try:
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
    except NoSuchElementException as e:
        print(f"Erreur : {e}")
    except Exception as e:
        print(str(e))

def find_elements(driver, criteria, element):
    try:
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
    except NoSuchElementException as e:
        print(f"Erreur : {e}")
    except Exception as e:
        print(str(e))

def smooth_move_to_element(driver, element):
    actions = ActionChains(driver)

    # Récupérer la position de l'élément
    element_location = element.location
    element_width = element.size['width']
    element_height = element.size['height']

    # Définir la destination au centre de l'élément
    target_x = element_location['x'] + element_width / 2
    target_y = element_location['y'] + element_height / 2

    # Obtenir la position actuelle de la souris
    current_x, current_y = driver.execute_script('return [window.scrollX, window.scrollY];')

    # Déterminer le nombre d'étapes et la distance entre chaque étape
    steps = 20
    delta_x = (target_x - current_x) / steps
    delta_y = (target_y - current_y) / steps

    # Simuler un mouvement fluide
    for i in range(steps):
        actions.move_by_offset(delta_x, delta_y)
        actions.perform()
        time.sleep(0.05)  # Petite pause pour rendre le mouvement plus naturel


def get_discount_percentage(last_price, actual_price):
    try:
        # Nettoyer les prix : supprimer le symbole $ et les espaces
        last = float(last_price.replace('$', '').strip().replace('.', ''))
        current = float(actual_price.replace('$', '').strip().replace('.', ''))

        # Calcul de la réduction
        discount = round((1 - (current / last)) * 100)
        discount = f"{discount}%"
        # Retour sous forme de string formatée
        return discount
    except (ValueError, ZeroDivisionError):
        return None

def destroy_intrusive_elements(driver):
    selectors = [
        '*[class*="popup"]',
        '*[id*="popup"]',
        '*[class*="modal"]',
        '*[id*="modal"]',
        '*[class*="overlay"]',
        '*[id*="overlay"]',
        '*[class*="cookie"]',
        '*[id*="cookie"]',
        '*[class*="banner"]',
        '*[id*="banner"]',
        '*[class*="ads"]',
        '*[id*="ads"]',
        'iframe',
        'div[role="dialog"]'
    ]
    
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for el in elements:
                driver.execute_script("arguments[0].remove();", el)
        except Exception:
            pass  # Ignore all exceptions, on ne veut rien savoir




# def translate(query):
#     # Traduire la requête directement en espagnol
#     translated_text = GoogleTranslator(source='auto', target='es').translate(query)
#     return translated_text


