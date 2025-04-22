from imports import *

fincaraiz_creds_path = r"C:\Users\f.gionnane\Documents\Selenium\fincaraiz Search\finca_raiz_creds.json"
with open(fincaraiz_creds_path, 'r') as file:
    content = json.load(file)
    email = content['email']
    password = content['password']




