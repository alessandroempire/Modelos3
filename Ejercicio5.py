import random
import simpy
from operator import attrgetter

""" Constantes de programa """
RANDOM_SEED       = 42      # La libreria de random requiere un seed
TIEMPO_SIMULACION = 365    	# La simulacion dura 30 dias

NUMERO_TERMINALES = 2 		# Existen N terminales en el puerto

tiempos_esperados = []

# COMO MODELAR LOS TIPOS DE BUQUE? UNA CLASE PARA CADA TIPO?


""" Clases de ayuda """
class Puerto():

    def __init__(self, env, numero_terminales):
        self.resource = simpy.Resource(env, capacity=2)
        self.terminales = []
        for i in range(numero_terminales):
            self.terminales.append(Terminal(chr(i + ord('A'))))

    def get_terminal(self):
        return self.terminales.pop(0)

    def add_terminal(self, terminal):
        self.terminales.append(terminal)

    def calcular_buques_servidos(self):
        total = 0
        for terminal in self.terminales:
            total += terminal.calcular_buques_servidos()
        return total


"""Clase para representar instancias de una terminal de puerto"""
class Terminal():
    def __init__(self, nombre):
        self.nombre = nombre
        self.buques_G_servidos = 0
        self.buques_M_servidos = 0
        self.buques_P_servidos = 0
        self.tiempo_trabajado = 0

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

