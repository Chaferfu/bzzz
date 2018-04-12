import sys
import re
import serial
import serial.tools.list_ports

TRASH_STATE = 1000 # Numero de l'etat poubelle (automate lexical)
        
# Automate LR(0) de l'analyseur syntaxique
# Chaque cle est representee par un tuple de la forme ["BEG", 8] ou
# "BEG" est le token lu, et 8 est l'etat actuel. La valeur en resultant
# decrit l'etat vers lequel aller, et si celle-ci est egale a 0, alors
# une reduction doit avoir lieu.
nb_members_LR = {}
nb_members_LR[3] = 1
nb_members_LR[7] = 3
nb_members_LR[10] = 1
nb_members_LR[11] = 1
nb_members_LR[12] = 1
nb_members_LR[13] = 3
nb_members_LR[15] = 3

syntax_LR = {}
syntax_LR["BEG", 1] = 2
syntax_LR["TYPE", 2] = 8
syntax_LR["SubData", 2] = 3
syntax_LR["Data", 2] = 4
syntax_LR["END", 3] = "Data"
syntax_LR["CUT", 3] = "Data"
syntax_LR["END", 4] = 5
syntax_LR["CUT", 4] = 6
syntax_LR["TYPE", 6] = 8
syntax_LR["SubData", 6] = 7
syntax_LR["END", 7] = "Data"
syntax_LR["CUT", 7] = "Data"
syntax_LR["CUT", 8] = 9
syntax_LR["NUM_INT", 9] = 11
syntax_LR["NUM_FLT", 9] = 12
syntax_LR["Value",9] = 10
syntax_LR["LValue", 9] = 13
syntax_LR["END", 10] = "LValue"
syntax_LR["CUT", 10] = "LValue"
syntax_LR["END", 11] = "Value"
syntax_LR["CUT", 11] = "Value"
syntax_LR["END", 12] = "Value"
syntax_LR["CUT", 12] = "Value"
syntax_LR["END", 13] = "SubData"
syntax_LR["CUT", 13] = 14
syntax_LR["NUM_INT", 14] = 11
syntax_LR["NUM_FLT", 14] = 12
syntax_LR["Value", 14] = 15
syntax_LR["END", 15] = "LValue"
syntax_LR["CUT", 15] = "LValue"
# Fin de l'automate

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

LValue ::= LValue CUT Value
|Value

Value ::= NUM_INT
|NUM_FLT

'''

# Trouve les ports COM utilisés et renvoie un tuple les contenant
def list_ports() :
    #list = serial.tools.list_ports.comports()
    connected = []
    #for element in list:
        #connected.append(element.device)
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
    
def syntaxical_analysis(tokens) :
    # Implementation de l'automate LR(0) de l'analyseur
    state = 1
    pile = []
    token_pile = []
    try :
        while len(tokens) > 0 :
            if state == 13 :
                if len(tokens) > 1 and tokens[1][0] == "TYPE" :
                    new_state = "SubData"
                else :
                     new_state = 14
            else :
                 new_state = syntax_LR[tokens[0][0], state]
            # Reduction
            if type(new_state) is str :
                member_count = nb_members_LR[state]
                for i in range(member_count) :
                    pile.pop()
                state = syntax_LR[new_state, pile[len(pile)-1]]
            else :
                state = new_state
                if tokens[0][0] in ("NUM_INT", "NUM_FLT", "TYPE") :
                    token_pile.append(tokens[0])
                del tokens[0]
            pile.append(state)
    except KeyError :
        print("Error : the message received is not correct...")
        return False
    # On cree l'arbre a partir de la pile de tokens
    return token_pile

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
            print("Port list : " + str(connected_ports))
            fp = open(sys.argv[1])
            data = fp.read()
            print(data)
            # Analyse lexicale
            tokens = lexical_analysis(data)
            # Analyse syntaxique
            token_list = syntaxical_analysis(tokens)
            # TODO : retirer ce print
            print(token_list)
        else :
            error_exit(error_list.no_port_error)
    else :
        print("Usage : python analyseur.py <file_to_read>")
