#Ca genere des trames aléatoires du format qu'on asdit qu'on fait 
import random as r
from datetime import datetime

#genere une trame random avecla date de maintenant
def generateRandomTrame(txErreur=0, randomSeed = 0):

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

	return trame

	

#renvoi un str de la date courante au format defini dans la trame
def getTimeString():
	time = str(datetime.now())
	time = time.replace("-","")
	time = time.replace(" ","")
	time = time.replace(":","")
	time = time.split(".")[0]
	return time


print(generateRandomTrame(0, datetime.now().microsecond))