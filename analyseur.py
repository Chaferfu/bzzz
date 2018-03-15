import sys


print(len(sys.argv))

fp = open(sys.argv[1])
data = fp.read()
print(data)

incr = 0
tokens = []

'''
différents tokens :

BEG : $
END : *$
TYPE : [a-z]
DATA : [0-9]*     	il faudra mettre un nombre fixe en fonction
					de la precision
CUT : {,}

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

def analyse_char(c, i):
	if c == '$' :
		tokens.append("BEG")

	if c == '*' :
		if (len(data) > i+1) & (data[i+1] == '$'):
			tokens.append("END")
			i+=1
		else :
	
			print("syntaxe incorrecte")
	i+=1
	return i

'''	if c == ',' :

	if c > 'a' & c < 'z' :

	if c > '0' & c < '9' :
'''


	
while incr < len(data) :
	incr = analyse_char(data[incr],incr)

print(tokens)
