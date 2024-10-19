from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserAccount  # Adjust this import based on your project structure




alphabetMin = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
alphabetMaj = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
specialCharacters = ["!","@","#","$","%","^","&","*","(",")","-","_","=","+","[","]","{","}","|","\\",":",";","'","\"",",",".","<",">","/","?","`","~"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


# Mot de passe de 3 charachtères de 0 à 2:

def motDePasseThreeChar():
    motDePasse = input("Entrer le mot de passe de 3 char de 0 à 2 :")
    while len(motDePasse) != 3 or not all(char in ['0', '1', '2'] for char in motDePasse):
        motDePasse = input("\033[91mEntrer un mot de passe de exactement 3 char de 0 à 2 !!\033[0m ")
    
    print("\033[92mMot de passe valide\033[0m")
    
#motDePasseThreeChar()


# Mot de passe de 6 charachtères de 0 à 9:

def motDePasseSixChar():
    motDePasse = input("Entrer le mot de passe de 6 char de 0 à 9 :")
    while len(motDePasse) != 6 or not all(char in numbers for char in motDePasse) :
        motDePasse = input("\033[91mEntrer un mot de passe de exactement 6 char de 0 à 9 !! \033[0m")
    
    print("\033[92mMot de passe valide\033[0m")
    
#motDePasseSixChar()

# Mot de passe de 6 charchtères de tous les chars :

def motDePasseMix(motDePasse):   
    if len(motDePasse) != 6 or not all(char in numbers + alphabetMaj + alphabetMin + specialCharacters for char in motDePasse):
        return False
    return True

     
#motDePasseMix()   




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
        if not motDePasseMix(password1) :
            raise forms.ValidationError("Password must have 6 charachters")
        return password1
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
            
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user