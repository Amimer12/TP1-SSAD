from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from .forms import CustomUserCreationForm, LoginForm
from .models import UserAccount
from django.views.decorators.csrf import csrf_exempt
import math


############################################ Affine Encrypt #######################################
def encrypt_message_affine(message, a, b):
    decimal_values_x = [ord(char) for char in message]  # Conversion en valeurs ASCII
    decimal_values_y = [a * value + b for value in decimal_values_x]  # Chiffrement
    encrypted_chars = [chr(value) for value in decimal_values_y]  # Conversion en caractères chiffrés
    encrypted_message = ''.join(encrypted_chars)  # Combinaison des caractères chiffrés
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
def PW_verification(password):
    special_characters = "(!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~)"

    digit = any(char.isdigit() for char in password)
    lower = any(char.islower() for char in password)
    upper = any(char.isupper() for char in password)
    special = any(char in special_characters for char in password)
    is_long_enough = len(password) >= 6

    if not digit:
        print("You should add a number to your password")
    if not lower:
        print("You should add a lowercase letter to your password")
    if not upper:
        print("You should add an uppercase letter to your password")
    if not special:
        print("You should add a special character to your password")
    if not is_long_enough:
        print("Your password should be at least 6 characters long")

    # Check if the password is strong or weak
    if digit and lower and upper and special and is_long_enough:
        return "your password is very strong"
    elif (digit and lower) or (upper and special) and is_long_enough:
        return "your password is strong"
    elif (digit and lower and not upper and not special) or (digit and upper and not lower and not special) \
            or (lower and upper and not digit and not special) or (digit and special and not lower and not upper) \
            or (lower and special and not digit and not upper) or (upper and special and not digit and not lower) \
            and is_long_enough:
        return "your password is weak"
    elif digit or lower or upper or special and is_long_enough:
        return "your password is very weak"
    else:
        return "your password is too weak"


def AuthPage(request):
    signup_form = CustomUserCreationForm()
    login_form = LoginForm()

    if request.method == "POST":
        
        # Handle user signup
        if 'username' in request.POST and 'email' in request.POST:
            signup_form = CustomUserCreationForm(request.POST)
            login_form = LoginForm()

            if signup_form.is_valid():
                # Verify password strength
                password = request.POST.get('password1')
                password_strength = PW_verification(password)

                if "very weak" in password_strength or "too weak" in password_strength:
                    return JsonResponse({'password_error': password_strength}, status=400)

                # If the password is acceptable, save the form
                signup_form.save()
                return JsonResponse({'success_message': "Your account has been successfully created!", 'password_strength': password_strength})
            else:
                errors = signup_form.errors.as_json()
                return JsonResponse({'errors': errors}, status=400)


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

            users = UserAccount.objects.all()
            user_found = False
            for user in users:
                if user.username == username and user.check_password(password):
                    user_found = True
                    print(f"User {username} authenticated successfully!")
                    return JsonResponse({'success_message': "Login successful!"})

            
            if not user_found:
                print("Authentication failed.")
                return JsonResponse({'errors': {'__all__': ["Please enter a correct username and password. Note that both fields may be case-sensitive."]}}, status=400)

################################################## LOGIN ###################################################
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
    
            
    else:
        signup_form = CustomUserCreationForm()
        login_form = LoginForm()

    return render(request, "index.html", {
        "signup_form": signup_form,
        "login_form": login_form
    })



