#Ca genere des trames aléatoires du format qu'on asdit qu'on fait 
import random as r
from datetime import datetime

#genere une trame random avecla date de maintenant
#txErreur a 
def generateRandomTrame(randomSeed=0, txErreur = 0):

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
	
	trame += "*$"

	#generation erreur
	if r.randint(0,100) < txErreur: #txErreur chances sur 100 de mettr eune erreur
		trame[r.randint(0,len(trame))] = r.choice(string.printable)

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
def genTrameFile(filename, randSeed = 0, txErreur = 0):

	with open(filename, "w") as f:

		time = datetime.now().microsecond

		for i in range(time,time+10000):
			f.write(generateRandomTrame(i, txErreur))
			f.write("\n")


