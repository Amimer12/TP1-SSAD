from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from .forms import CustomUserCreationForm, LoginForm
from .models import UserAccount
from .models import FailedLoginAttempt
from django.views.decorators.csrf import csrf_exempt
import math
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now


# ******************************* Fonction pour calculer l'inverse modulaire de a ######################################
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Pas d'inverse modulaire pour a={a} et m={m}")

# ************************ Vérifier si a est coprime avec 128 (pour éviter des erreurs de déchiffrement)###########
def is_coprime(a, m):
    return math.gcd(a, m) == 1

# *********************** Fonction pour chiffrer un message (Affine)
def encrypt_message(message, a, b):
    decimal_values_y = []
    m = 128

    if not is_coprime(a, m):
        raise ValueError(f"Erreur : a doit être coprime avec {m} pour que le chiffrement fonctionne.")

    # Liste des valeurs décimales avec les valeurs ASCII des caractères de message
    decimal_values_x = [ord(char) for char in message]

    # Chiffrer chaque caractère avec modulo 128
    for value in decimal_values_x:
        encrypted_value = (a * value + b) % m
        decimal_values_y.append(encrypted_value)

    # Convertir les valeurs décimales chiffrées en caractères
    encrypted_message = ''.join([chr(value) for value in decimal_values_y])

    return encrypted_message

# *********************** Fonction pour déchiffrer un message (Affine)#####################################
def decrypt_message(encrypted_message, a, b):
    m = 128
    decimal_values_z = []
    
    # Calculer l'inverse modulaire de a
    a_inv = mod_inverse(a, m)

    # Liste des valeurs décimales du message chiffré
    z = [ord(char) for char in encrypted_message]

    # Déchiffrer chaque caractère avec modulo 128
    for value in z:
        decrypted_value = (a_inv * (value - b)) % m
        decimal_values_z.append(decrypted_value)

    # Convertir les valeurs décimales déchiffrées en caractères
    decrypted_message = ''.join([chr(value) for value in decimal_values_z])

    return decrypted_message

############################  Décalage : ##############################################################

def decalage_droite_mot(mot):
    """Décale tous les caractères d'un mot à droite d'un caractère."""
    if len(mot) == 0:
        return mot
    return mot[-1] + mot[:-1]

def decalage_gauche_mot(mot):
    """Décale tous les caractères d'un mot à gauche d'un caractère."""
    if len(mot) == 0:
        return mot
    return mot[1:] + mot[0]

def decalage_texte(texte):
    """Décale chaque mot du texte à droite et à gauche."""
    mots = texte.split()
    
    # Décalage à droite pour tous les mots
    mots_droite = [decalage_droite_mot(mot) for mot in mots]
    texte_droite = ' '.join(mots_droite)

    # Décalage à gauche pour tous les mots
    mots_gauche = [decalage_gauche_mot(mot) for mot in mots]
    texte_gauche = ' '.join(mots_gauche)

    return texte_droite, texte_gauche

# Exemple d'utilisation
#message = "Hello world Python"
#print("Message original:", message)

# Décalage
#decalage_d, decalage_g = decalage_texte(message)
#print("Décalage à droite:", decalage_d)
#print("Décalage à gauche:", decalage_g)

########################### Mirroir ######################################

def mirroir(text):
    result = text[::-1]
    return(result if text != result else decalage_texte(text))


def AuthPage(request):
    signup_form = CustomUserCreationForm()
    login_form = LoginForm()

    if request.method == "POST":
        
        # Handle user signup
        if 'username' in request.POST and 'email' in request.POST:
            signup_form = CustomUserCreationForm(request.POST)
            login_form = LoginForm()

            if signup_form.is_valid():
                signup_form.save()
                return JsonResponse({'success_message': "Your account has been successfully created!"})
            else:
                errors = signup_form.errors.as_json()
                return JsonResponse({'errors': errors}, status=400)
            
############################### LOGIN FUNCTION ###########################################################
        elif 'username' in request.POST and 'password' in request.POST:
            login_form = LoginForm(request, data=request.POST)
            signup_form = CustomUserCreationForm()

            username = login_form.data.get('username')
            password = login_form.data.get('password')

            print(f"Attempting to authenticate user: {username}")
            
            try:
                user = UserAccount.objects.get(username=username)
            except UserAccount.DoesNotExist:
                return JsonResponse({'errors': {'__all__': ["Invalid username."]}}, status=400)
            #users = UserAccount.objects.all()
            #user_found = False
            #for user in users: user.username == username and
            if user :  
            # verfier si utlisateure son compte n'est pas blocker 
                failed_attempt,create= FailedLoginAttempt.objects.get_or_create(user=user)

                if failed_attempt.is_locked():
                    remaining_time = failed_attempt.locked_until - now()
                    minutes_remaining = remaining_time.total_seconds() 
                    print("account blocked")
                    return JsonResponse({'errors': {'__all__': [f"Your account is locked. Try again  in {int(minutes_remaining)} seconde."]}}, status=403)
 
                if  user.check_password(password):
                    failed_attempt.reset_attempts()
                    #user_found = True
                    print(f"User {username} authenticated successfully!")
                    return JsonResponse({'success_message': "Login successful!"})
                else :
                    print("Authentication failed.")
                    failed_attempt.attempts += 1
                    print(failed_attempt.attempts)
                # Si 3 tentatives échouées, verrouiller pendant 30 minutes
                    if failed_attempt.attempts >= 3:
                        failed_attempt.lock_account()
                        return JsonResponse({'errors': {'__all__': ["Too many failed attempts. Account locked for 30 seconde"]}}, status=403)
                    
                    failed_attempt.save()
                    print("Authentication failed.")
                    return JsonResponse({'errors': {'__all__': ["invalide password"]}}, status=400)
           # if not user_found:
           
#####################################################################################################
        elif 'method' in request.POST and 'textToEncrypt' in request.POST:
            method = request.POST.get('method')
            textToEncrypt = request.POST.get('textToEncrypt')
            CryptedText = ""
            if method and textToEncrypt :
                if method == '1':
                    CryptedText = mirroir(textToEncrypt)
                elif method =="2":
                    pass
                elif method =="3":
                    CryptedText = decalage_gauche_mot(textToEncrypt)
                elif method =="4":
                    CryptedText = decalage_droite_mot(textToEncrypt)
                elif method == "5":
                    pass
                
                return JsonResponse({'success':True,'CryptedText': CryptedText })
            else:
                return JsonResponse({'errors': "An error occurred. Please try again."}, status=400)

                
            
    else:
        signup_form = CustomUserCreationForm()
        login_form = LoginForm()

    return render(request, "index.html", {
        "signup_form": signup_form,
        "login_form": login_form
    })



