from imports import *
from constants import *

# Fonction pour récupérer le code de vérification depuis l'email
def get_verification_code():
    service = build('gmail', 'v1', credentials=authenticate_gmail())
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread from:no-reply@exito.com").execute()
    messages = results.get('messages', [])
    if not messages:
        print('No new messages.')
    else:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            msg_body = msg['payload']['headers']
            for part in msg['payload']['parts']:
                try:
                    if part['filename']:
                        pass  # Handle attachments here if needed
                    else:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        code_match = re.search(r'\b\d{6}\b', body)
                        if code_match:
                            return code_match.group()  # Return the first 6-digit code found
                except KeyError:
                    pass
    return None


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
















