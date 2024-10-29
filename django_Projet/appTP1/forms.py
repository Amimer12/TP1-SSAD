from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserAccount  # Adjust this import based on your project structure


################################################ MOT DE PASSE FUNCTIONS #########################################################

alphabetMin = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
alphabetMaj = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
specialCharacters = ["!","@","#","$","%","^","&","*","(",")","-","_",
    "=","+","[","]","{","}","|","\\",":",";","'","\"",",",".","<",">","/","?","`","~"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


# Mot de passe de 3 charachtères de 0 à 2:

def motDePasseThreeChar(motDePasse):
    
    if len(motDePasse) != 3 or not all(char in ['0', '1', '2'] for char in motDePasse):
        return False, "Password must have 3 characters that are 0, 1, or 2!"
    return True, ""
    
# Mot de passe de 6 charachtères de 0 à 9:

def motDePasseSixChar(motDePasse):
    
    if len(motDePasse) != 6 or not all(char in numbers for char in motDePasse) :
       return False, "Password must have 6 characters between 0 and 9!"
    return True, ""


# Mot de passe de 6 charchtères de tous les chars :

def motDePasseMix(motDePasse):   
    if len(motDePasse) != 6 or not all(char in numbers + alphabetMaj + alphabetMin + specialCharacters for char in motDePasse):
        return False, "Password must have 6 characters of letters, numbers, or special characters!"
    return True, ""


##################################################################################################################################
def PW_verification(password):
    digit = any(char.isdigit() for char in password)
    lower = any(char.islower() for char in password)
    upper = any(char.isupper() for char in password)
    special = any(char in specialCharacters for char in password)
    is_long_enough = len(password) >= 6

    if not digit:
        return False,"You should add a number to your password"
    if not lower:
        return False,"You should add a lowercase letter to your password"
    if not upper:
        return False,"You should add an uppercase letter to your password"
    if not special:
        return False,"You should add a special character to your password"
    if not is_long_enough:
        return False,"Your password should be at least 6 characters long"

    # Check if the password is strong or weak
    if digit and lower and upper and special and is_long_enough:
        return True,"your password is very strong"
    elif (digit and lower) or (upper and special) and is_long_enough:
        return True,"your password is strong"
    elif (digit and lower and not upper and not special) or (digit and upper and not lower and not special) \
            or (lower and upper and not digit and not special) or (digit and special and not lower and not upper) \
            or (lower and special and not digit and not upper) or (upper and special and not digit and not lower) \
            and is_long_enough:
         return False,"your password is weak"
    else:
        return False,"your password is very weak"
    

## CREATE ACCOUNT FORM ##############################################

class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ('email', 'username')  

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        is_valid, error_message = motDePasseThreeChar(password1)
        if not is_valid:
            raise forms.ValidationError(error_message)
        return password1
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords doesn't match")
            
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
#########################################################################################


## LOGIN FORM ###########################################################################

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Username',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password',
            'class': 'form-control'
        })
    )



#########################################################################################
