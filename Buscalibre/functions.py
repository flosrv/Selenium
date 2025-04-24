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

def find_child_elements(element):
    wait = WebDriverWait(element, 10)
    child = wait.until(EC.presence_of_element_located((By.XPATH,"*/.." )))
    return child

def find_parent_element(element):
    wait = WebDriverWait(element,10)

    children = wait.until(EC.presence_of_element_located((By.XPATH,"./.." )))
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
        wait = WebDriverWait(driver, 10)
        
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
        element = wait.until(EC.presence_of_element_located((by_map[criteria], element)))
        return element
    
    except NoSuchElementException as e:
        print(f"Erreur : {e}")
    except Exception as e:
        print(str(e))


def find_elements(driver_or_element, criteria, selector):
    try:
        criteria = criteria.strip().lower()
        wait = WebDriverWait(driver_or_element, 10)

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

        # Attente de présence d'au moins un élément
        wait.until(EC.presence_of_element_located((by_map[criteria], selector)))

        # Récupération de tous les éléments correspondants
        elements = driver_or_element.find_elements(by_map[criteria], selector)
        return elements if elements else []

    except Exception as e:
        print(f"❌ find_elements error : {e}")
        return []

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


def translate(query):
    # Traduire la requête directement en espagnol
    translated_text = GoogleTranslator(source='auto', target='es').translate(query)
    return translated_text


def process_string(query):
    query = query.lower().strip()
    query = unidecode(query)
    query = GoogleTranslator(source='auto', target='es').translate(query)
    return query



def wait_page_to_load(driver):
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def safe_get_text(parent, xpath, key=None, book_details=None, label=None, attr=None, timeout=10):
    try:
        # Attente explicite de l'élément
        el = WebDriverWait(parent, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        
        # Extraire la valeur
        val = el.get_attribute(attr).strip() if attr else el.text.strip()
        
        # Ajouter au dictionnaire si nécessaire
        if book_details is not None and key:
            book_details[key] = val
        
        # Affichage du label si nécessaire
        if label:
            print(f"{label}: {val}")
        
        return val
    except Exception as e:
        # Gestion des erreurs et affichage
        if label:
            print(f"❌ Erreur sur {label} :\n{str(e)}")
        return None

def get_book_details(driver):
    book_details = {}
    print("📄 Page chargée avec succès.")
    
    products_listings = find_element(driver, "xpath", "//div[contains(@class, 'productos')]")
    cards = find_elements(products_listings, "xpath", "//div[contains(@class, 'box-producto') and contains(@data-id_producto, '')]")
    card = cards[0]

    title = safe_get_text(card, ".//h3[contains(@class, 'nombre')]", "Title", book_details, "Title")
    href = safe_get_text(card, ".//a[contains(@href, '')]", "Link", book_details, "Link", attr="href")
    autor = safe_get_text(card, ".//div[contains(@class, 'autor')]", "Autor", book_details, "Author")
    edition = safe_get_text(card, ".//div[contains(@class, 'autor') and contains(@class,'color-dark-gray')]", "Edition", book_details, "Edition")
    

    price = safe_get_text(card, ".//p[contains(@class, 'precio-ahora')]", "Actual Price", book_details, "Price")

    try:
        precio_antes = find_element(card, "xpath", ".//p[contains(@class, 'precio-antes')]").text.strip()
        book_details["Old Price"] = precio_antes
        print(f"Old Price: {precio_antes}\n")
        match_digit_precio = re.search(r'\d+\.\d+', price)
        match_digit_precio_antes = re.search(r'\d+\.\d+', precio_antes)
        if match_digit_precio and match_digit_precio_antes:
            match_digit_precio = match_digit_precio.group()
            match_digit_precio_antes = match_digit_precio_antes.group()
        discount_value = 100 - int(100 * float(match_digit_precio) / float(match_digit_precio_antes))
        discount = f"{discount_value}%"
        book_details["Discount"] = discount
        print(f"Discount: {discount}")
    except:
        print("Old Price not found")
    print("Going to product page...")

    ####### GO ON PRODUCT PAGE ######################################################################################################################################################

    driver.get(href)
    wait_page_to_load(driver)
    print("📄 Page produit chargée avec succès.")

    try:
        info_libro = find_element(driver, "xpath", "//div[contains(@id, 'data-info-libro')]")
        book_year = safe_get_text(driver, 
            "//div[contains(@class, 'box') and contains(@id, 'metadata-ano')]", "year", book_details, "📅 Année de publication")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des informations du livre :\n{e}")

    try:
        place_star_rate = find_element(info_libro, "xpath", "//span[contains(@class, 'stars')]")
        match_star_rate = re.search(r'\d{1,2}', place_star_rate.get_attribute("class"))
        if match_star_rate:
            star_rate = match_star_rate.group()
            book_details["star_rate"] = star_rate
            print(f"⭐ Note du livre : {star_rate} étoiles")
    except Exception as e:
        print(f"❌ Erreur sur la note du livre :\n{e}")

    try:
        rating_amount = find_element(driver, "xpath", "//a[contains(@class, 'valoracion')]").text
        match_rating_amount = re.search(r'\d+', rating_amount.replace('.', '').replace(',', ''))
        if match_rating_amount:
            rating_amount = match_rating_amount.group()
            book_details["rating_amount"] = rating_amount
        print(f"📊 Nombre d'avis : {rating_amount}")
    except Exception as e:
        print(f"❌ Erreur sur le nombre d'avis :\n{e}")

    try:
        stocks_details = safe_get_text(card, ".//p[contains(@class, 'stock')]", "Stock", book_details, "Stock status")
        if stocks_details:
            print(f"📦 Stock status: {stocks_details}")
            
    except Exception as e:
        print(f'Stock not found:\n{str(e)}')
    try:
        details = find_element(driver, "xpath", "//div[contains(@id, 'detallePrecio')]")
        sending_date = find_elements(details, "xpath", ".//strong[contains(@style, 'green')]")
        sending_date = f"{sending_date[0].text.strip()} - {sending_date[1].text.strip()}"
        book_details["sending_date"] = sending_date
        print(f"📦 Date d'envoi estimée : {sending_date}")
    except Exception as e:
        print(f"❌ Erreur sur la date d'envoi :\n{e}")

    try:
        book_description = find_element(details, "xpath", "//span[contains(@id,'texto-descripcion')]").text.strip()
        book_details["description"] = book_description
        print(f"📚 Description du livre : {book_description}")
    except Exception as e:
        print(f"❌ Erreur sur la description : {e}")
        

    try:
        author_description = find_element(driver, "xpath", ".//div[contains(@class, 'biography')]").text.strip()
        book_details["author_description"] = author_description
        print(f"👨‍🏫 Description de l'auteur : {author_description}")
    except Exception as e:
        print(f"❌ Erreur sur la description de l'auteur : {e}")

    percentages_by_star = get_star_percentage(driver)
    book_details["star_percentages"] = percentages_by_star

    try:
        mas_infos = find_element(details, "xpath", ".//div[contains(@class, 'texto-mas-info')]")
        if mas_infos.is_displayed():
            mas_infos.click()
            modal = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "modalMasInfo1")))
            origin = modal.find_element(By.XPATH, ".//strong[contains(text(), 'Origen')]").text.replace("Origen:", "").strip()
            book_details["origin"] = origin
            print(f"🌍 Origine : {origin}")
            sending_dates = modal.find_elements(By.XPATH, ".//strong[contains(text(), 'Martes') or contains(text(), 'Lunes')]")
            sending_date_start = sending_dates[0].text.strip()
            sending_date_end = sending_dates[1].text.strip()
            book_details["sending_dates"] = f"{sending_date_start} - {sending_date_end}"
            print(f"📅 Dates d'envoi estimées : {sending_date_start} - {sending_date_end}")
            delivery_note = modal.find_element(By.XPATH, ".//div[contains(text(), 'Lo recibirás')]").text.strip()
            book_details["delivery_note"] = delivery_note
            print(f"📦 Détails de livraison : {delivery_note}")
    except Exception as e:
        print(f"❌ Erreur sur les informations supplémentaires :\n{e}")

    return book_details

def get_star_percentage(driver):
    # Wait for the page to load
    driver.implicitly_wait(10)  # Waits for 10 seconds

    # Dictionnaire pour stocker les pourcentages par étoiles
    star_percentages = {}

    # Find the element containing the evaluation stars
    evaluations_repartition = find_element(driver, "xpath", "//div[contains(@class, 'reviews-body-resume')]")
    
    # Get all the li elements that correspond to each star rating (1, 2, 3, 4, 5 stars)
    each_star = find_elements(evaluations_repartition, "xpath", ".//li[contains(@class, 'stars-')]")

    # Variables pour calculer la note générale pondérée
    total_percentage = 0
    total_stars = 0

    # Loop through each star and extract the star rating and percentage
    for star in each_star:
        # Extract the class attribute to get the star rating (e.g., stars-5)
        class_attr = star.get_attribute("class")
        match_star = re.search(r'stars-(\d)', class_attr)
        
        if match_star:
            star_rating = match_star.group(1)
            
            try:
                # Find the percentage div (under the div with class 'percent-parent')
                percent_div = find_element(star, "xpath", ".//div[contains(@class, 'percent-parent')]//div[contains(@class, 'percent')]")
                # Get the style attribute of the div to extract the width (percentage)
                style_attr = percent_div.get_attribute("style")
                
                # Use regex to extract the percentage width (e.g., "width: 83.33%;")
                match_percentage = re.search(r'width:\s*(\d+(?:\.\d+)?)%', style_attr)
                
                if match_percentage:
                    percentage = match_percentage.group(1) + '%'
                    print(f"⭐ {star_rating} étoiles : {percentage}")
                    # Ajouter l'information dans le dictionnaire
                    star_percentages[star_rating] = percentage
                    
                    # Calculer la note générale pondérée
                    percentage_value = float(match_percentage.group(1))  # Convertir en valeur numérique
                    total_percentage += percentage_value * int(star_rating)  # Pondérer par le nombre d'étoiles
                    total_stars += percentage_value  # Pondérer par la somme des pourcentages
                else:
                    print(f"❌ Pourcentage non trouvé pour {star_rating} étoiles")
            except Exception as e:
                print(f"❌ Erreur sur la récupération du pourcentage pour {star_rating} étoiles : {e}")
        else:
            print("❌ Classe d'étoile non trouvée")

    # Calculer la note générale (pondérée)
    if total_stars > 0:
        weighted_average = total_percentage / total_stars
    else:
        weighted_average = 0  # Si aucune donnée n'a été trouvée, retourner 0 comme note générale

    # Ajouter la note générale au dictionnaire
    star_percentages["Overall Rating"] = round(weighted_average, 2)
    print(f"⭐ Note générale : {star_percentages['Overall Rating']} stars")
    # Retourner le dictionnaire des pourcentages par étoiles et la note générale
    return star_percentages


