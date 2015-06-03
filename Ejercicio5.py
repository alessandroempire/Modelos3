import random
import simpy
from operator import attrgetter

""" Constantes de programa """
RANDOM_SEED       = 42      # 
TIEMPO_SIMULACION = 365    	# La simulacion dura 30 dias

NUMERO_TERMINALES = 2 		# Existen N terminales en el puerto

tiempos_esperados = []


class Puerto():
    def __init__(self, env, numero_terminales):
        self.resource = simpy.Resource(env, capacity=2)
        self.terminales = ['A', 'B']
        #for i in range(numero_terminales):
        #    self.terminales.append(Terminal(chr(i + ord('A'))))

    def get_terminal(self):
        return self.terminales.pop(0)

    def add_terminal(self, terminal):
        self.terminales.append(terminal)

    def calcular_buques_servidos(self):
        total = 0
        for terminal in self.terminales:
            total += terminal.calcular_buques_servidos()
        return total

"""Clase que representa un terminal"""
class Terminal():
    def __init__(self, nombre):
        self.nombre = nombre
        self.buques_G_servidos = 0
        self.buques_M_servidos = 0
        self.buques_P_servidos = 0
        self.tiempo_trabajado  = 0

    def calcular_tiempo_buque(self, tipo_buque):
        tiempo_trabajado = 0
        if self.nombre == 'A':
            if tipo_buque == 'G':
                tiempo_trabajado = 4
                self.tiempo_trabajado += 4
                self.buques_G_servidos += 1
            elif tipo_buque == 'M':
                tiempo_trabajado = 3
                self.tiempo_trabajado += 3
                self.buques_M_servidos += 1
            elif tipo_buque == 'P':
                tiempo_trabajado = 2
                self.tiempo_trabajado += 2
                self.buques_P_servidos += 1
        elif self.nombre == 'B':
            if tipo_buque == 'G':
                tiempo_trabajado = 3
                self.tiempo_trabajado += 3
                self.buques_G_servidos += 1
            elif tipo_buque == 'M':
                tiempo_trabajado = 2
                self.tiempo_trabajado += 2
                self.buques_M_servidos += 1
            elif tipo_buque == 'P':
                tiempo_trabajado = 1
                self.tiempo_trabajado += 1
                self.buques_P_servidos += 1
        return tiempo_trabajado

    def calcular_buques_servidos(self):
        return self.buques_G_servidos + self.buques_M_servidos + \
            self.buques_P_servidos

def tiempo_llegada():
    dias = 0 
    rand = random.randint(0, 100)

    if 0 <= rand <= 20:
        dias = 1
    elif 20 < rand <= 45:
        dias = 2
    elif 45 < rand <= 80:
        dias = 3 
    elif 80 < rand <= 95:
        dias = 4
    elif 95 < rand <= 100:
        dias = 5

    return dias

def tipo_buque():
    buque = ''
    rand = random.randint(0,100)

    if 0 <= rand <= 40:
        buque = 'G'
    elif 40 < rand <= 75:
        buque = 'M'
    elif 75 < rand <= 100:
        buque = 'P'

    return buque

def generator(env, puerto):
    contador_buques = 0 
    
    while True:
        type_buque = tipo_buque()
        dias       = tiempo_llegada()

        env.process(buque(env, ('Buque %02d' % contador_buques), 
                    type_buque, puerto))

        yield env.timeout(dias)

        contador_buques += 1

def buque(env, nombre_buque, tipo_buque, puerto):
    global tiempos_esperados
    
    llegada = env.now





###############################################################################

print('Ejercicio 5 \n')

env = simpy.Environment()

