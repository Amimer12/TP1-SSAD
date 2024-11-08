from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from .forms import CustomUserCreationForm, LoginForm
from .models import UserAccount
from django.views.decorators.csrf import csrf_exempt
from .models import FailedLoginAttempt
from django.utils.timezone import now
from .cryptage_methods import *
from .steganography_methods import *
from captcha.image import ImageCaptcha
import random
import string
import io
import base64

def generate_captcha_text(length=6):
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
#################################################################################################################

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
            captcha = login_form.data.get('captcha_text')
            captha_verfication = login_form.data.get('captha_verfication')
            print(captha_verfication)

            if captha_verfication == "true":
                print(f"{captcha} and {request.session.get('captcha_text')}")
                if request.session.get('captcha_text') != captcha : 
                    return JsonResponse({'errors': {'__all__': ["Invalid captcha"]}}, status=400)

            print(f"Attempting to authenticate user: {username}")
            
            try:
                user = UserAccount.objects.get(username=username)
            except UserAccount.DoesNotExist:
                return JsonResponse({'errors': {'__all__': ["Invalid username."]}}, status=400)

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
           
################################################## CRYPTAGE ###################################################
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
                        if mod_inverse(affine_a, 26):

                            CryptedText = encrypt_message_affine(textToEncrypt, affine_a, affine_b)
                            if CryptedText:
                                DecryptedText = decrypt_message_affine(CryptedText, affine_a, affine_b)
                        else:
                            error_msg = "L'inverse de A n'existe pas. Assurez-vous que A et 26 sont premiers entre eux."    
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
                        
                
                if CryptedText and DecryptedText:
                    return JsonResponse({'success': True, 'CryptedText': CryptedText, 'DecryptedText': DecryptedText})
                
            else:
                error_msg = "Method and text to encrypt must be provided."
            return JsonResponse({'errors': error_msg}, status=400)
    
    #################################  STEGANOGRAPHY ########################################################""

        elif 'methodStg' in request.POST and 'textToStg' in request.POST: 
            methodStg = request.POST.get('methodStg')
            textToStg = request.POST.get('textToStg')
            nbr_column = request.POST.get('nbr_column')
            messageStg = ""
            error_msg = ""
            
            # Check if both method and text are provided
            if not methodStg or not textToStg:
                error_msg = "Method and text must be provided."
            elif methodStg =="s3" and not nbr_column:
                error_msg = "You have to enter the number of columns for this method to work"
            elif not check_text_length(textToStg):  # Check if text length is sufficient
                error_msg = "Your text must contain at least 30 words!"
            else:
                # Process the message extraction based on the chosen method
                if methodStg == "s1":
                    messageStg = decode_message_from_invisible_characters(textToStg)
                    if not messageStg :
                        error_msg = "No hidden message detected !"
                elif methodStg == "s2":
                    messageStg = extraire_message_phrase(textToStg)
                elif methodStg == "s3":
                    messageStg = extraire_message_colonne(textToStg, int(nbr_column))
            
            # Return success or error messages in JSON response
            if messageStg:
                return JsonResponse({'success': True, 'messageStg': messageStg})
            else:
                return JsonResponse({'errors': error_msg}, status=400)

            

        elif 'methodStgHide' in request.POST and 'textToStgHide' in request.POST and 'MsgStgHide' in request.POST: 
            methodStgHide = request.POST.get('methodStgHide')
            textToStgHide = request.POST.get('textToStgHide')
            MsgStgHide = request.POST.get('MsgStgHide')
            nbr_columns = request.POST.get('nbr_column') if methodStgHide == "s3" else None

            TextWithHiddenMessage = ""
            error_msg = ""

            # Check for missing required fields
            if not methodStgHide or not textToStgHide or not MsgStgHide:
                error_msg = "Method, text, and message are required."
            elif not check_text_length(textToStgHide):  # Ensure text has at least 30 words
                error_msg = "Your text must contain at least 30 words!"
            else:
                # Process the hiding message methods based on the chosen method
                if methodStgHide == "s1":
                    TextWithHiddenMessage,error_msg = encode_message_with_invisible_characters(textToStgHide, MsgStgHide)
                    if error_msg != "":
                        TextWithHiddenMessage = ""
                elif methodStgHide == "s2":
                    TextWithHiddenMessage,error_msg = steg_phrase(MsgStgHide, textToStgHide)
                    if error_msg != "":
                        TextWithHiddenMessage = ""
                elif methodStgHide == "s3" and nbr_columns:
                    TextWithHiddenMessage,error_msg = steg_colonne(MsgStgHide, textToStgHide,int(nbr_columns))
                    if error_msg != "":
                        TextWithHiddenMessage = ""
                else:
                    error_msg = "Number of columns is required for this method."

            # Return success or error messages in JSON
            if TextWithHiddenMessage:
                return JsonResponse({'success': True, 'TextWithHiddenMessage': TextWithHiddenMessage})
            else:
                return JsonResponse({'errors': error_msg}, status=400)

            

    else:
        signup_form = CustomUserCreationForm()
        login_form = LoginForm()
        
    ## generer captcha 
    captcha_text = generate_captcha_text()
    image = ImageCaptcha(width=280, height=90)
    captcha_image = image.generate_image(captcha_text)
    buffer = io.BytesIO()
    captcha_image.save(buffer, format='PNG')
    captcha_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    request.session['captcha_text'] = captcha_text
    return render(request, "index.html", {
        "signup_form": signup_form,
        "login_form": login_form,
        'captcha_image': captcha_image_base64,
    })

