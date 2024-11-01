import math

def check_text_length(text):
    words = text.split()
    return len(words) >= 30

############################################### STGANOGRAPHY INIVSIBLE CHARACHTERS ##################################################################################
def encode_message_with_invisible_characters(text, message):
    binary_message = ''.join(f"{ord(char):08b}" for char in message)
    encoded_text = []

    bit_index = 0
    mots = text.split()
    error_message =""
    if len(mots) < len(binary_message):
        error_message = (F"it's impossible to hide your message in this text cause it contains less words than the length of your message, insert more words or shorter message !")
    
    for char in text:
        encoded_text.append(char)
        
        if bit_index < len(binary_message):
            if binary_message[bit_index] == '1':
                encoded_text.append('\u200B') 
            else:
                encoded_text.append('\u200C')  
            bit_index += 1
    
    return ''.join(encoded_text),error_message

def decode_message_from_invisible_characters(encoded_text):
    binary_message = ""
    
    for char in encoded_text:        
        if char == '\u200B':  
            binary_message += '1'
        elif char == '\u200C':  
            binary_message += '0'

    decoded_chars = [chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)]
    return ''.join(decoded_chars)

############################################### STGANOGRAPHY PAR PHRASE #########################################

def steg_phrase(secret, text):
    phrases = text.split('.')
    error_message = ""
    if len(phrases) < len(secret):
       error_message = (F"It's impossible to hide your message in this text cause it contains {len(phrases)} sentences, insert more sentences or shorter message !")

    textSteg = []
    for index, phrase in enumerate(phrases):
        if index < len(secret):
           phraseSteg = secret[index] + phrase[1:]
        else:
           phraseSteg = phrase 
        textSteg.append(phraseSteg)

    textSteg = '.'.join(textSteg)
    return textSteg ,error_message


def extraire_message_phrase(texte_cache):
    phrases = texte_cache.split(".")
    message_revele = ''.join(phrase[0] for phrase in phrases if phrase)
    return message_revele

############################################### STGANOGRAPHY PAR COLONNE #########################################
import math

def steg_colonne(secret, text, nb_colonnes):
    mots = text.split()
    error_message =""
    if len(mots) < len(secret):
        error_message = (F"it's impossible to hide your message in this text cause it contains less words than the length of your message, insert more words or shorter message !")
    
    nb_lignes = math.ceil(len(mots) / nb_colonnes)
    tableau = text_to_tab(mots, nb_colonnes, nb_lignes)
    index_message = 0
    zero_width_space = '\u200B'  
    for j in range(nb_colonnes):
        for i in range(nb_lignes):
            if index_message < len(secret) and tableau[i][j]:  
                tableau[i][j] = secret[index_message] + zero_width_space + tableau[i][j][1:]
                index_message += 1
    
    texte_cache = " ".join(" ".join(ligne) for ligne in tableau)
    return texte_cache.strip(),error_message

def extraire_message_colonne(text_cache, nb_colonnes):
    mots = text_cache.split()
    nb_lignes = math.ceil(len(mots) / nb_colonnes)
    tableau = text_to_tab(mots, nb_colonnes, nb_lignes)
    message_extrait = ""
    zero_width_space = '\u200B'  

    for j in range(nb_colonnes):
        for i in range(nb_lignes):
            if tableau[i][j]: 
                if len(tableau[i][j]) > 1 and tableau[i][j][1] == zero_width_space:
                    message_extrait += tableau[i][j][0] 
    
    return message_extrait.strip()

def text_to_tab(mots, nb_colonnes, nb_lignes):
    tableau = [["" for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
    index = 0
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            if index < len(mots):
                tableau[i][j] = mots[index]
                index += 1
    return tableau



# Example usage
text = """Politics is the process by which societies make collective decisions,
shaping laws, policies, and governance structures that impact everyone.
At its core, politics is about power—who has it, how it’s used, and the
values that guide it. In democratic systems, it often involves debates
between different parties or groups with competing ideologies, where 
leaders are chosen by citizens to represent their interests. owever, 
poltical systems can range from emocracies to autocracies, each with 
varying egrees of citizn participation and governmet accountability.
In today's world, politics also intersects with pressing global issues 
like climate change, economic inequality, and human rights, making it a 
dynamic and often contentious field."""

