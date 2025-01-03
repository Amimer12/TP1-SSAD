
############################################ Affine Encrypt #######################################
def encrypt_message_affine(message, a, b):
    def affine_encrypt_char(char):
         if char == " ":
           return '$'  # Replace spaces with $
         if char.isalpha():
             
            # Pour les lettres majuscules
            if char.isupper():
                return chr(((a * (ord(char) - ord('A')) + b) % 26) + ord('A'))
            else:
                return chr(((a * (ord(char) - ord('a')) + b) % 26) + ord('a'))
         else:
            return char  # Les autres caractères ne sont pas modifiés
    
    encrypted_chars = [affine_encrypt_char(char) for char in message]  # Chiffrement
    encrypted_message = ''.join(encrypted_chars)  # Combinaison des caractères chiffrés
    return encrypted_message


############################################ Affine Decrypt ############################################
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
 
def mod_inverse(a, m):
    if gcd(a, m) != 1:
        return None
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def decrypt_message_affine(encrypted_message, a, b):
    a_inv = mod_inverse(a, 26)
    def affine_decrypt_char(char):
        if char == '$':
            return " "
        elif char.isalpha():
            if char.isupper():
                return chr(((a_inv * (ord(char) - ord('A') - b)) % 26 + 26) % 26 + ord('A'))
            else:
                return chr(((a_inv * (ord(char) - ord('a') - b)) % 26 + 26) % 26 + ord('a'))
        else:
            return char

    decrypted_chars = [affine_decrypt_char(char) for char in encrypted_message]
    decrypted_message = ''.join(decrypted_chars)
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
            if n % 10 == 0 :
                texte_crypte += chr((ord(caractere) - 1 - 48) % 10 + 48)
            else:
                texte_crypte += chr((ord(caractere) - n - 48) % 10 + 48)
           
        # crypter les lettres majuscules
        elif caractere.isupper():
            if n % 26 == 0 :
                texte_crypte += chr((ord(caractere) - 1 - 65) % 26 + 65)
            else:
                texte_crypte += chr((ord(caractere) - n - 65) % 26 + 65)
        # crypter les lettres minuscules
        elif caractere.islower():
            if n % 26 == 0  :
                texte_crypte += chr((ord(caractere) - 1 - 97) % 26 + 97)
            else:
                texte_crypte += chr((ord(caractere) - n - 97) % 26 + 97)
        # crypter les caractères spéciaux
        else:
            index = caracteres_speciaux.index(caractere)
            if n % 35 == 0 :
                texte_crypte += caracteres_speciaux[(index - 1) % 35]
            else:
                texte_crypte += caracteres_speciaux[(index - n) % 35]
    return texte_crypte


def encrypt_cesar_adroite(texte, n):
    texte_crypte = ""
    caracteres_speciaux = [" ","—","’", "!", '"', "#", "$", "%", "&", "`", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "'", "{", "|", "}", "~"]

    for caractere in texte:
        # crypter les chiffres
        if caractere.isdigit():
            if n % 10 == 0 :
                texte_crypte += chr((ord(caractere) + 1 - 48) % 10 + 48)
            else:
                texte_crypte += chr((ord(caractere) + n - 48) % 10 + 48)
        # crypter les lettres majuscules
        elif caractere.isupper():
            if n % 26 == 0:
                texte_crypte += chr((ord(caractere) + 1 - 65) % 26 + 65)
            else:
                texte_crypte += chr((ord(caractere) + n - 65) % 26 + 65)
        # crypter les lettres minuscules
        elif caractere.islower():
            if n % 26 == 0:
                texte_crypte += chr((ord(caractere) + 1 - 97) % 26 + 97)
            else:
                texte_crypte += chr((ord(caractere) + n - 97) % 26 + 97)
        # crypter les caractères spéciaux
        else:
            index = caracteres_speciaux.index(caractere)
            if n % 35 == 0:
                texte_crypte += caracteres_speciaux[(index + 1) % 35]
            else:
                texte_crypte += caracteres_speciaux[(index + n) % 35]
    return texte_crypte


def decrypt_cesar_agauche(texte, n):
    texte_decrypte = ""
    caracteres_speciaux = [" ","—","’", "!", '"', "#", "$", "%", "&", "`", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "'", "{", "|", "}", "~"]

    for caractere in texte:
        # décrypter les chiffres
        if caractere.isdigit():
            if n % 10 == 0 :
                texte_decrypte += chr((ord(caractere) + 1 - 48) % 10 + 48)
            else:
                texte_decrypte += chr((ord(caractere) + n - 48) % 10 + 48)
        # décrypter les lettres majuscules
        elif caractere.isupper():
            if n % 26 == 0 :
                texte_decrypte += chr((ord(caractere) + 1 - 65) % 26 + 65)
            else:
                texte_decrypte += chr((ord(caractere) + n - 65) % 26 + 65)
        # décrypter les lettres minuscules
        elif caractere.islower():
            if n % 26 == 0 :
                texte_decrypte += chr((ord(caractere) + 1 - 97) % 26 + 97)
            else:
                texte_decrypte += chr((ord(caractere) + n - 97) % 26 + 97)
        # décrypter les caractères spéciaux
        else:
            index = caracteres_speciaux.index(caractere)
            if n % 35 == 0 :
                texte_decrypte += caracteres_speciaux[(index + 1) % 35]
            else:
                texte_decrypte += caracteres_speciaux[(index + n) % 35]
    return texte_decrypte


def decrypt_cesar_adroite(texte, n):
    texte_decrypte = ""
    caracteres_speciaux = [" ","—","’", "!", '"', "#", "$", "%", "&", "`", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "'", "{", "|", "}", "~"]

    for caractere in texte:
        # décrypter les chiffres
        if caractere.isdigit():
            if n % 10 == 0 :
                texte_decrypte += chr((ord(caractere) - 1 - 48) % 10 + 48)
            else:
                texte_decrypte += chr((ord(caractere) - n - 48) % 10 + 48)
        # décrypter les lettres majuscules
        elif caractere.isupper():
            if n % 26 == 0 :
                texte_decrypte += chr((ord(caractere) - 1 - 65) % 26 + 65)
            else:
                texte_decrypte += chr((ord(caractere) - n - 65) % 26 + 65)
        # décrypter les lettres minuscules
        elif caractere.islower():
            if n % 26 == 0 :
                texte_decrypte += chr((ord(caractere) - 1 - 97) % 26 + 97)
            else:
                texte_decrypte += chr((ord(caractere) - n - 97) % 26 + 97)
        # décrypter les caractères spéciaux
        else:
            index = caracteres_speciaux.index(caractere)
            if n % 35 == 0 :
                texte_decrypte += caracteres_speciaux[(index - 1) % 35]
            else:
                texte_decrypte += caracteres_speciaux[(index - n) % 35]
    return texte_decrypte
