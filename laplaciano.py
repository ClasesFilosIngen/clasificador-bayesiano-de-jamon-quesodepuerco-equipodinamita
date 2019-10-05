# In[26]:
#Hernandez Ibanez Miguel Angel
#Hernandez Romero Pompeyo 
import re 
import numpy
k=1
def limpiaPalabras(oracion):#limpia la oracion, eliminando mayusculas y separando palabras
	palabras=re.sub("[^\w]", " ", oracion).split()
	oracionLimpia=[p.lower() for p in palabras]
	return oracionLimpia

def bagOfWords(listaOraciones): #hacemos la bolsa de palabras 
	bag={}
	for oracion in listaOraciones:
		palabras=limpiaPalabras(oracion)
		for p in palabras: 
			if p not in bag.keys():
				bag[p]=1
			else: 
				bag[p]+=1
	return bag
#por ahora hace una bolsa de palabras, rellenando las bolsas de spam y ham con los valores 0
def subBag(sub1, univ): 
	sub={}
	sub=sub1 
	for l in univ.keys():
		if l not in sub.keys():
			sub[l]=0
		else: 
			sub[l]=sub[l]
	return sub
#cuenta las palabras de cada diccionario
def contPalabras(dic):
	cont=0
	for val in dic.keys():
			if dic[val]>0: 
				cont+=dic[val]
	return cont
#prob spam/universo
def probXY(a, b):
	prob=(a+k)/(b+(k*2))
	return prob
#probabilidad de cada palabra en los diccionarios
def probDic(dic, a,x):
	for val in dic.keys(): 
		dic[val]=(dic[val]+k)/(a+(k*x))
	return dic
#calculamos la probabilidad de p(spam o ham|| palabra)
def primerClasificacion(palabra, dicEval, probEval, probWinUniv): 
	p=0
	pWinDic=0
	pWinUniv=0
	if palabra in dicEval.keys(): 
		pWinDic=dicEval.get(palabra)
	else: 
		return "no se encontro la palabra"
	if palabra in probWinUniv.keys():
		pWinUniv=probWinUniv.get(palabra)
	else: 
		return "no se encontro la palabra"
	p=(pWinDic*probEval)/pWinUniv
	return p
def probM(oracion, pSpam, pHam, dicSpam, dicHam):
	pS=1
	pH=1
	pOrSpam=0
	pals=limpiaPalabras(oracion)
	for p in pals:
		if p in dicSpam.keys():
			pS*=dicSpam.get(p)
	pS*=pSpam
	for p in pals:
		if p in dicHam.keys():
			pH*=dicHam.get(p)
	pH*=pHam
	pT=(pS)+(pH)
	pOrSpam=pS/pT
	pOrHam=pH/pT
	return [pT, pOrSpam, pOrHam]
#def laplaciano(): 
def main(): 
	universe=[]
	bagSpam={}
	bagUniverse={}
	bagHam={}
	newSpam={}
	newHam={}
	aux={}
	newUniverse={}
	contSpam=0
	contHam=0
	oracion=[]
	correo="practica es evento"

	spam=["Oferta es secreto","Clik link secreto", "link deportes secreto"]
	ham=["practica deportes hoy", "fue practica deportes", "deportes evento secreto", "deportes es hoy", "deportes cuesta dinero"]

#Haciendo el universo de palabras
	universe.extend(ham)
	universe.extend(spam)
	tamUniverse=len(universe)
	tamHam=len(ham)
	tamSpam=len(spam)
#Calculamos la probabilidad de spam y ham
	probSpam=probXY(tamSpam, tamUniverse)
	#print(probSpam)
	probHam=probXY(tamHam, tamUniverse)
	#print(probHam)
#hacemos la bolsa de palabras para 
	bagSpam=bagOfWords(spam)
	bagHam=bagOfWords(ham)
	bagUniverse=bagOfWords(universe)
#variable para las clases del laplaciano
	x1=len(bagUniverse)
#completamos la bolsa de palabras con valores nulos
	newSpam=subBag(bagSpam, bagUniverse)
	newHam=subBag(bagHam, bagUniverse)
#hacemos el conteo de cada diccionario 
	contSpam=contPalabras(newSpam)
	#print(contSpam)
	contHam=contPalabras(newHam)
	#print(contHam)
	contUniverse=contPalabras(bagUniverse)
	aux=newHam.copy()
#esperando que no se modifique el newHam
	probDic(aux, contHam, x1)
	newHam=aux
	aux=newSpam.copy()
#esperando que no se modifique el newSpam
	aux=newSpam.copy()
	probDic(aux, contSpam,x1)
	#print(newHam)
	newSpam=aux
	#print(newSpam)
#esperando que no se modifique el newSpam
	aux=bagUniverse.copy()
	probDic(aux, contUniverse,x1)
	newUniverse=aux
#p(spam| "secreto")
	pSecretoSpam=primerClasificacion("secreto", newSpam, probSpam, newUniverse)
	#print(pSecretoSpam)
#p(ham|secreto)
	pSecretoHam=primerClasificacion("secreto", newHam, probHam, newUniverse)
	#print(pSecretoHam)
	oracion=probM(correo, probSpam, probHam, newSpam, newHam)
	print("La probabilidad de que aparezca la oracion '" +correo+ "' en un correo es %0.5f: "% (oracion[0]))
	print("La probabilidad de que el correo sea spam es %0.5f: "%(oracion[1]))
	print("La probabilidad de que el correo sea ham es %0.5f: "%(oracion[2]))
main()
# In[ ]: