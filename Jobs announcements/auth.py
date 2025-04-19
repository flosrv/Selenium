from imports import *

computrabajo_creds_path = r"C:\Users\f.gionnane\Documents\Selenium\Jobs announcements\connection_creds.json"
with open(computrabajo_creds_path, 'r') as file:
    content = json.load(file)
    email = content['email']
    password = content['password']






















