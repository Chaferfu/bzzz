#Ca genere des trames aléatoires du format qu'on asdit qu'on fait 
import random as r
from datetime import datetime
import sys
import string

#genere une trame random avecla date de maintenant
#txErreur a 
def generateRandomTrameFromPresent(randomSeed=0, txErreur = 0):

	r.seed(randomSeed)

	trame = "$"

	trame += "h,"
	trame += getTimeString() + ","

	#tempartures en millidegre celsuic
	trame += "t,"
	for i in range(1, r.randint(2,5)):
		trame += str(r.randint(5000,30000)) + ","
		

	#pressions en pascal
	trame += "p,"
	for i in range(1, r.randint(2,5)):
		trame += str(r.randint(100000,100099)) + ","
	
	trame = trame[:len(trame)-1]
	trame += "*$"

	#generation erreur
	if r.randint(0,100) < txErreur: #txErreur chances sur 100 de mettr eune erreur
		liste = list(trame)
		liste[r.randint(0,len(liste)-1)] = r.choice(string.printable)
		trameTumefiee = "".join(liste)
		return trameTumefiee

	return trame

	

#renvoi un str de la date courante au format defini dans la trame
def getTimeString():
	time = str(datetime.now())
	time = time.replace("-","")
	time = time.replace(" ","")
	time = time.replace(":","")
	time = time.split(".")[0]
	return time

#genere un fichier rempli de trames random
def genTrameFile(filename, randSeed = datetime.now().microsecond, txErreur = 0):

	with open(filename, "w") as f:

		for i in range(randSeed,randSeed+10000):
			f.write(generateRandomTrameFromPresent(i, txErreur))
			f.write("\n")

#prend une trame, la tumefie et la renvoie dans un etat de bug total
def tumefierTrame(trame):
	liste = list(trame)
	liste[r.randint(0,len(liste))] = r.choice(string.printable)
	trameTumefiee = "".join(liste)
	return trameTumefiee

if __name__ == "__main__" :
	if len(sys.argv) >= 2 :
		filename = sys.argv[1]
		genTrameFile(filename, datetime.now().microsecond, 20)
	else :
		print("Usage : python genTrame.py <filename>")
