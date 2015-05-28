import random
import simpy
from operator import attrgetter

""" Clase que representa un agente """

class Agente():
	def __init__(self, numero):
		self.numero         = numero
		self.nombre         = "Agente %02d" % numero
		self.autos_vendidos = 0
		self.comision       = 0

""" Clase que representa un automovil """

class Automovil():
	def __init__(self, modelo):
		self.modelo = modelo

""" Variables del programa"""
RANDOM_SEED       = 42     #El random necesita un seed
TIEMPO_SIMULACION = 0      # ??
NUMERO_AGENTES    = 5       
autos_vendidos    = 0 
agentes           = [Agente(1), Agente(2), Agente(3), Agente(4), Agente(5)]

""" Funciones del sistema """

def ventaSemanal():
	global autos_vendidos #se usa variable global

	rand = random.randint(0, 100)

	if 0 <= rand <= 10:
		autos_vendidos = 0
	elif 10 < rand <= 25:
		autos_vendidos = 1
	elif 25 < rand <= 45:
		autos_vendidos = 2
	elif 45 < rand <= 70:
		autos_vendidos = 3
	elif 70 < rand <= 90 :
		autos_vendidos = 4
	elif 90 < rand <= 100:
		autos_vendidos = 5

	return autos_vendidos

def tipoCarro():

	rand = random.randint(0,100) 

	if 0 <= rand <= 40:
		car = Automovil('Compacto')
	elif 40 < rand <= 75:
		car = Automovil('Mediano')
	elif 75 < rand <= 100:
		car = Automovil('Lujo')

	return car

def calculoComision(auto, agente):
	if auto.modelo == 'Compacto':
		agente.comision += 250
	elif auto.modelo == 'Mediano':
		rand = random.randint(0,100)
		if 0 <= rand <= 40:
			agente.comision += 400
		elif 40 < rand <= 100:
			agente.comision += 500
	elif auto.modelo == 'Lujo':
		rand = random.randint(0,100)
		if 0 <= rand <= 35:
			agente.comision += 1000
		elif 35 < rand <= 75:
			agente.comision += 1500
		elif 75 < rand <= 100:
			agente.comision += 2000

## Ejecucion principal
print("Ejercicio 8 \n")


for i in agentes:
	autos = ventaSemanal()
	car   = tipoCarro()
	#para el numero de carro vendidos
	# calcular el tipo de carro
	# y luego a cada carro
	# calcular comision
	calculoComision(car, agente(i))

# sumar todo y sacar promedio ;) 