import sys
import re
import serial
import serial.tools.list_ports

TRASH_STATE = 1000 # Numero de l'etat poubelle (automate lexical)

class error_list :
    no_port_error = "no port is used or available"
    syntaxic_error = "some characters of the data are not correctly written, data may be corrupted"

'''
différents tokens :

BEG : $
END : *$
TYPE : [a-z]
NUM_INT : [0-9]+            il faudra mettre un nombre fixe en fonction
                            de la precision si que des entiers (flottants trasformes en entiers)
NUM_FLT : [0-9]+ . [0-9]+ 
CUT : {,}                   

format d'un token : 
[<TOKEN_TYPE> , <TOKEN_VALUE>]  pour les tokens TYPE, NUM_INT et NUM_FLT
[<TOKEN_TYPE>]                  pour tous les autres tokens
'''

'''

règles de grammaire :

String ::= BEG Data END
Data ::= Data CUT SubData
|SubData

SubData ::= TYPE CUT LValue

LValue ::= LValue CUT DATA
|DATA

'''

# Trouve les ports COM utilisés et renvoie un tuple les contenant
def list_ports() :
    list = serial.tools.list_ports.comports()
    connected = []
    for element in list:
        connected.append(element.device)
    return connected

# Transforme les informations recuperes en tokens
def lexical_analysis(data):
    char_pos = 0
    tokens = [] 
    ignored_char = [" ", "\n", "\t"]
    c = "" # Caractere lu
    NUM_value = "" # Pour recuperer un nombre envoye
    TYPE_token = re.compile("[a-z]")
    NUM_token = re.compile("[0-9]")
    state = 0 # Etat initial
    i = 0 # Curseur dans le string
    ''' 
    Automate de l'analyse lexical
        
    Se referer la documentation pour voir l'automate complet
    '''
    while i < len(data) :
        c = data[i]
        # On ignore les espace
        if c not in ignored_char :
            # Etat initial
            if state == 0 :
                if c == '$' :
                    tokens.append(["BEG"])
                elif c == ',' :
                    tokens.append(["CUT"])
                elif TYPE_token.match(c) :
                    tokens.append(["TYPE", c])
                elif c == '*' :
                    state = 1 
                elif NUM_token.match(c) :
                    NUM_value += c
                    state = 2
                else :
                    state = TRASH_STATE
            
            # Etat du caractere de sortie
            elif state == 1 :
                if c == '$' :
                    state = 0
                    tokens.append(["END"])
                else :
                    state = TRASH_STATE
            
            # Etat nombre entier
            elif state == 2 :
                if NUM_token.match(c) :
                    NUM_value += c
                elif c == '.' :
                    NUM_value += c
                    state = 3
                else :
                    tokens.append(["NUM_INT", NUM_value])
                    NUM_value = ""
                    state = 0
                    i = i-1
                    
            # Etat nombre flottant
            elif state == 3 :
                if NUM_token.match(c) :
                    NUM_value += c
                else : 
                    tokens.append(["NUM_FLT", NUM_value])
                    NUM_value = ""
                    state = 0
                    i = i-1
            
            # Etat poubelle : envoie une erreur
            elif state == TRASH_STATE :
                # TODO : changer le comportement de l'erreur (redemander un paquet)
                error_exit(error_list.syntaxic_error + ", misplaced character : " + "\'" + c + "\'" + " at number " + str(i+1))
        if state != TRASH_STATE :
            i += 1
    return tokens
    
def error_exit(error_msg) :
    print("Error : " + error_msg + "\nExiting the program...")
    exit()

if __name__ == "__main__" :
    if len(sys.argv) >= 2 and type(sys.argv[1]) is str :
        # Recuperation des ports utilises
        connected_ports = list_ports()
        # Ouverture du port utilise si existant
        if len(connected_ports) >= 0 : # En realite >= 1
            #~ ser = serial.Serial(connected_ports[0], 9600, timeout=1)
            #~ print("Port list : " + str(connected_ports))
            fp = open(sys.argv[1])
            data = fp.read()
            print(data)
            # Analyse syntaxique
            tokens = lexical_analysis(data)
            print(tokens)
        else :
            error_exit(error_list.no_port_error)
    else :
        print("Usage : python analyseur.py <file_to_read>")
