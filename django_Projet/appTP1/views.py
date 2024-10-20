from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from .forms import CustomUserCreationForm, LoginForm
from .models import UserAccount
from django.views.decorators.csrf import csrf_exempt
import math


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

#####################################################################################################

    else:
        signup_form = CustomUserCreationForm()
        login_form = LoginForm()

    return render(request, "index.html", {
        "signup_form": signup_form,
        "login_form": login_form
    })


# ******************************* Fonction pour calculer l'inverse modulaire de a
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Pas d'inverse modulaire pour a={a} et m={m}")

# ************************ Vérifier si a est coprime avec 128 (pour éviter des erreurs de déchiffrement)
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

# *********************** Fonction pour déchiffrer un message (Affine)
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
