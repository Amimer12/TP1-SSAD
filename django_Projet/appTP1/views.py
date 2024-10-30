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


############################################ Affine Encrypt #######################################
def encrypt_message_affine(message, a, b):
    decimal_values_x = [ord(char) for char in message]  # Conversion en valeurs ASCII
    decimal_values_y = [a * value + b for value in decimal_values_x]  # Chiffrement
    encrypted_chars = [chr(value) for value in decimal_values_y]  # Conversion en caractères chiffrés
    encrypted_message = ''.join(encrypted_chars)  # Combinaison des caractères chiffrés


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


############################################ Affine Decrypt ############################################
def decrypt_message_affine(encrypted_message, a, b):
    decimal_values_z = [ord(char) for char in encrypted_message]  # Conversion en valeurs ASCII chiffrées
    decimal_values_decrypted = [(value - b) // a for value in decimal_values_z]  # Déchiffrement
    decrypted_chars = [chr(value) for value in decimal_values_decrypted]  # Conversion en caractères déchiffrés
    decrypted_message = ''.join(decrypted_chars)  # Combinaison des caractères déchiffrés
    return decrypted_message

############################################ Décalage ##############################################
def encrypt_decalage_droite(mot):
    """Décale tous les caractères d'un mot à droite d'un caractère. Gère plusieurs mots."""
    words = mot.split(" ")  
    result_words = []
    
    for word in words:
        if len(word) == 0:
            result_word = word
        else:
            result_word = word[-1] + word[:-1]
            if word == result_word:  
                result_word = encrypt_cesar_adroite(word, 1)
        result_words.append(result_word)
    
    return " ".join(result_words)  # Join the words back with spaces

def encrypt_decalage_gauche(mot):
    """Décale tous les caractères d'un mot à gauche d'un caractère. Gère plusieurs mots."""
    words = mot.split(" ")
    result_words = []
    
    for word in words:
        if len(word) == 0:
            result_word = word
        else:
            result_word = word[1:] + word[0]
            if word == result_word:
                result_word = encrypt_cesar_agauche(word, 1)
        result_words.append(result_word)
    
    return " ".join(result_words)

def decrypt_decalage_droite(mot):
    """Décale tous les caractères d'un mot à droite d'un caractère (inverse). Gère plusieurs mots."""
    words = mot.split(" ")
    result_words = []
    
    for word in words:
        result_word = encrypt_decalage_gauche(word)  # Use gauche to reverse droite
        if word == result_word:
            result_word = decrypt_cesar_adroite(word, 1)
        result_words.append(result_word)
    
    return " ".join(result_words)

def decrypt_decalage_gauche(mot):
    """Décale tous les caractères d'un mot à gauche d'un caractère (inverse). Gère plusieurs mots."""
    words = mot.split(" ")
    result_words = []
    
    for word in words:
        result_word = encrypt_decalage_droite(word)  # Use droite to reverse gauche
        if word == result_word:
            result_word = decrypt_cesar_agauche(word, 1)
        result_words.append(result_word)
    
    return " ".join(result_words)


############################################ Mirroir ###########################################

def mirroir_cryptage(text):
    mots=text.split()
    resultats=[]
    
    for mot in mots:
        result = mot[::-1]
        if mot.lower()==result.lower():
            taille=len(mot)
            partie_centrale=mot[taille//2:]
            if taille%2 == 0:
                result="y"+partie_centrale +"xx"
            else:
                result="y"+partie_centrale +"x" 
        resultats.append(result)
    return ' '.join(resultats)

def mirroir_decryptage(text):
    mots=text.split()
    resultats=[]
    for mot in mots:
        if mot.startswith('y') and mot.endswith('xx'):
            partie_centrale=mot[1:-2]
            original=partie_centrale[::-1]+partie_centrale
        elif mot.startswith('y') and mot.endswith('x'):
            partie_centrale=mot[1:-1]
            original=partie_centrale[::-1]+partie_centrale[1::]
        else:
            original=mot[::-1]
        resultats.append(original)
    return ' '.join(resultats)

############################################ César #############################################

#methode1: en utilisant table d'ascii
'''
def cryptage_cesar(texte,n):
    texte_crypte=""
    for caractere  in texte :
        texte_crypte += chr((ord(caractere )+n-32)%95+32)
    return texte_crypte

def decryptage_cesar(texte,n):
    texte_noncrypte=""
    for caractere  in texte :
        texte_noncrypte += chr((ord(caractere )-n-32)%95+32)
    return texte_noncrypte
'''
#methode2:
def encrypt_cesar_agauche(texte, n):
    texte_crypte = ""
    caracteres_speciaux = [" ","—","’", "!", '"', "#", "$", "%", "&", "`", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "'", "{", "|", "}", "~"]

    for caractere in texte:
        # crypter les chiffres
        if caractere.isdigit():
            texte_crypte += chr((ord(caractere) - n - 48) % 10 + 48)
        # crypter les lettres majuscules
        elif caractere.isupper():
            texte_crypte += chr((ord(caractere) - n - 65) % 26 + 65)
        # crypter les lettres minuscules
        elif caractere.islower():
            texte_crypte += chr((ord(caractere) - n - 97) % 26 + 97)
        # crypter les caractères spéciaux
        else:
            index = caracteres_speciaux.index(caractere)
            texte_crypte += caracteres_speciaux[(index - n) % 33]
    return texte_crypte


def encrypt_cesar_adroite(texte, n):
    texte_crypte = ""
    caracteres_speciaux = [" ","—","’", "!", '"', "#", "$", "%", "&", "`", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "'", "{", "|", "}", "~"]

    for caractere in texte:
        # crypter les chiffres
        if caractere.isdigit():
            texte_crypte += chr((ord(caractere) + n - 48) % 10 + 48)
        # crypter les lettres majuscules
        elif caractere.isupper():
            texte_crypte += chr((ord(caractere) + n - 65) % 26 + 65)
        # crypter les lettres minuscules
        elif caractere.islower():
            texte_crypte += chr((ord(caractere) + n - 97) % 26 + 97)
        # crypter les caractères spéciaux
        else:
            index = caracteres_speciaux.index(caractere)
            texte_crypte += caracteres_speciaux[(index + n) % 33]
    return texte_crypte


def decrypt_cesar_agauche(texte, n):
    texte_decrypte = ""
    caracteres_speciaux = [" ","—","’", "!", '"', "#", "$", "%", "&", "`", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "'", "{", "|", "}", "~"]

    for caractere in texte:
        # décrypter les chiffres
        if caractere.isdigit():
            texte_decrypte += chr((ord(caractere) + n - 48) % 10 + 48)
        # décrypter les lettres majuscules
        elif caractere.isupper():
            texte_decrypte += chr((ord(caractere) + n - 65) % 26 + 65)
        # décrypter les lettres minuscules
        elif caractere.islower():
            texte_decrypte += chr((ord(caractere) + n - 97) % 26 + 97)
        # décrypter les caractères spéciaux
        else:
            index = caracteres_speciaux.index(caractere)
            texte_decrypte += caracteres_speciaux[(index + n) % 33]
    return texte_decrypte


def decrypt_cesar_adroite(texte, n):
    texte_decrypte = ""
    caracteres_speciaux = [" ","—","’", "!", '"', "#", "$", "%", "&", "`", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "'", "{", "|", "}", "~"]

    for caractere in texte:
        # décrypter les chiffres
        if caractere.isdigit():
            texte_decrypte += chr((ord(caractere) - n - 48) % 10 + 48)
        # décrypter les lettres majuscules
        elif caractere.isupper():
            texte_decrypte += chr((ord(caractere) - n - 65) % 26 + 65)
        # décrypter les lettres minuscules
        elif caractere.islower():
            texte_decrypte += chr((ord(caractere) - n - 97) % 26 + 97)
        # décrypter les caractères spéciaux
        else:
            index = caracteres_speciaux.index(caractere)
            texte_decrypte += caracteres_speciaux[(index - n) % 33]
    return texte_decrypte


########################################################################################################################################

#################################################################################################################################

def decode_message_from_invisible_characters(encoded_text):
    binary_message = ""
    
    for char in encoded_text:        
        if char == '\u200B':  
            binary_message += '1'
        elif char == '\u200C':  
            binary_message += '0'

    decoded_chars = [chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)]
    return ''.join(decoded_chars)



def AuthPage(request):
    signup_form = CustomUserCreationForm()
    login_form = LoginForm()

    if request.method == "POST":
        
        # Handle user signup
        if 'username' in request.POST and 'email' in request.POST :
            signup_form = CustomUserCreationForm(request.POST)
            login_form = LoginForm()

            if signup_form.is_valid():
                signup_form.save()
                return JsonResponse({'success_message': "Your account has been successfully created!"})
            else:
                errors = signup_form.errors.as_json()
                return JsonResponse({'errors': errors}, status=400)

############################### LOGIN FUNCTION ###########################################################
        elif 'username' in request.POST and 'password' in request.POST :
            
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
            cesar_key = int(request.POST.get('cesar_key')) if request.POST.get('cesar_key') else None
            affine_a = int(request.POST.get('affine_a')) if request.POST.get('affine_a') else None
            affine_b = int(request.POST.get('affine_b')) if request.POST.get('affine_b') else None
            CryptedText = ""
            DecryptedText = ""
            error_msg = ""

        
            if (method and textToEncrypt) or CryptedText == "":
                if method == '1':  # Mirroir method
                    CryptedText = mirroir_cryptage(textToEncrypt)
                    if CryptedText:
                        DecryptedText = mirroir_decryptage(CryptedText)

                elif method == '2':  # Affine method

                    if affine_a is not None and affine_b is not None:
                        if affine_a > 0:
                            CryptedText = encrypt_message_affine(textToEncrypt, affine_a, affine_b)
                            if CryptedText:
                                DecryptedText = decrypt_message_affine(CryptedText, affine_a, affine_b)
                        else:
                            error_msg = "A value must be superior than 0 !"
                    else:
                        error_msg = "You must enter A and B so the method works!"

                elif method == '3':  # Decalage gauche method
                    CryptedText = encrypt_decalage_gauche(textToEncrypt)
                    if CryptedText:
                        DecryptedText = decrypt_decalage_gauche(CryptedText)

                elif method == '4':  # Decalage droite method
                    CryptedText = encrypt_decalage_droite(textToEncrypt)
                    if CryptedText:
                        DecryptedText = decrypt_decalage_droite(CryptedText)

                elif method == '5':  # Cesar à gauche method
                    if cesar_key is not None:
                        CryptedText = encrypt_cesar_agauche(textToEncrypt, cesar_key)
                        if CryptedText:
                            DecryptedText = decrypt_cesar_agauche(CryptedText, cesar_key)
                    else:
                        error_msg = "You have to enter the Cesar key so the method works!"

                elif method == '6':  # Cesar à droite method
                    if cesar_key is not None:
                        CryptedText = encrypt_cesar_adroite(textToEncrypt, cesar_key)
                        if CryptedText:
                            DecryptedText = decrypt_cesar_adroite(CryptedText, cesar_key)
                    else:
                        error_msg = "You have to enter the Cesar key so the method works!"
                
                # Handle success response
                if CryptedText and DecryptedText:
                    return JsonResponse({'success': True, 'CryptedText': CryptedText, 'DecryptedText': DecryptedText})
                

            else:
                error_msg = "Method and text to encrypt must be provided."

            # Return error if something goes wrong
            return JsonResponse({'errors': error_msg}, status=400)
    
        elif 'methodStg' in request.POST and 'textToStg' in request.POST: 
            methodStg = request.POST.get('methodStg')
            textToStg = request.POST.get('textToStg')
            messageStg = ""
            if methodStg and textToStg :
                if methodStg == "1":
                    messageStg = decode_message_from_invisible_characters(textToStg)
                
            else:
                error_msg = "Method and text to encrypt must be provided."
            if messageStg:
                    return JsonResponse({'success': True, 'messageStg': messageStg})

    else:
        signup_form = CustomUserCreationForm()
        login_form = LoginForm()

    return render(request, "index.html", {
        "signup_form": signup_form,
        "login_form": login_form
    })



