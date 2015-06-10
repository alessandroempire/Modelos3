import random
import math
import simpy

""" Variables del problema"""
maquinas  = [1,2,3,4]
repuestos = [5,6,7]
areparar  = []

""" Constantes de ayuda"""
SIM_TIME = 500
semaforo = True
time     = 0

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
    y=random.uniform(0,1)
    return (-1)*math.log(1-y)
    
def generator(env, reparador, maquinas, repuestos, areparar):
	global time, semaforo

	while True:
		if semaforo :
			# lo que tarda en danarse!
			t = gFuncionandoDano()

			yield env.timeout(t)

			# saco la maquina se se dano y la ponga en la
			# la lista de reparar
			m = maquinas.pop()
			areparar.append(m)

			# saco una de repuesto y la pongo a funcionar
			mr = repuestos.pop()
			maquinas.append(mr)

			#mando a reparar la maquina danada!
			env.process(reparando(env, reparador, repuestos, 
				                  areparar))

			#si no hay mas repuesto se acabo la simulacion
			if (len(repuestos) == 0):
				semaforo = False
				time = env.now

		else: 
			#forzar que acabe la simulacion
			fin = env.now
			yield env.timeout(SIM_TIME - fin)
			continue

def reparando(env, reparador, repuestos, areparar):
	# Solo un tipo a la vez repara
	with reparador.request() as req:
		yield req

		#tiempo de reparar
		t = gReparar()

		yield env.timeout(t)

		#saco una maquina de las que se esta reparando
		# y las coloco com repuesto
		m = areparar.pop()
		repuestos.append(m)


############################################################
print('Ejercicio 4 \n')

env = simpy.Environment()

reparador = simpy.Resource(env, capacity=1)

env.process(generator(env, reparador, maquinas, 
	                  repuestos, areparar))

env.run(until=SIM_TIME)

print("Tiempo de simulacion %f" %time)