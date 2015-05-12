import random
import math

maquinas =[1,2,3,4]
repuestos = [5,6,7]
areparar=[]

def media(l):
	m = t = 0
	tam = len(l)
	# Calculo de la media
	for i in l:
		m += i

	media = m / tam
	return media

def desv(l):
	m = media(l)
	t = 0
	tam = len(l)
	for i in l:
		t += math.pow((i - m), 2)

	varianza = t / (tam -1)
	desv = math.sqrt(varianza)	
	return desv

def intervalo(l):
	m = media(l)
	d = desv(l)
	tam = len(l)
	inf = m - (1.96 * (d / math.sqrt(tam)))
	sup = m + (1.96 * (d / math.sqrt(tam)))
	inter = [inf, sup]
	return inter

def gReparar():
    x=random.uniform(0,1)
    return (-0.5)*math.log(1-x)
 
#Tiempo que tarda una pieza funcionando hasta danarse.
def gFuncionandoDano():
    xx=random.uniform(0,1)
    return (-1)*math.log(1-xx)
    
def main():
	
	n = 5 # Numero de simulaciones
	t1=[]
	for i in range (0,n):
		danado= gFuncionandoDano()
		tr=0
		for k in range (0,15):
			
			if danado <= 0: 
				
				danado = gFuncionandoDano()   
				areparar.append(maquinas.pop(0))
				if (len(repuestos)>0):
					maquinas.append(repuestos.pop(0))
				else:
					break

			else: 
				danado -= 1
				
			tr -=1
			if tr<=0 :
				if len(areparar)>0 :
				   repuestos.append(areparar.pop(0))
				   tr= gReparar()
		t1.append(k)
	h= media(t1)
	hh=desv(t1)
	hhh= intervalo(t1)
	print "La media fue"
	print h, "dias"
	print "La desviacion estandar es "
	print hh
	print " El intervalo de confianza es"
	print hhh

print('Ejercicio 4 \n')
main()

    

     