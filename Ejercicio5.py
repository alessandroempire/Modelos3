import random
import simpy
import math
from operator import attrgetter

""" Constantes de programa """
RANDOM_SEED       = 42      
TIEMPO_SIMULACION = 30    	# un a~o de simulacion

NUMERO_TERMINALES = 2 		# Existen N terminales en el puerto

tiempos_esperados = []

class Puerto():
    def __init__(self, env, numero_terminales):
        self.resource = simpy.Resource(env, capacity=numero_terminales)
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
    dias = 1
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
    buque = 'G'
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
    print ('init')
    
    while True:
        type_buque = tipo_buque()
        print('tipo %s' %type_buque)
        dias       = tiempo_llegada()  #dias que tarda en llegar
        print('dias1 %f' %dias)

        yield env.timeout(dias) 

        env.process(buque(env, ('Buque %02d' % contador_buques), 
                          type_buque, puerto) )        

        #yield env.timeout(dias) #muevo el tiempo unidad: dias

        contador_buques += 1
        print('next buque')

def buque(env, nombre_buque, tipo_buque, puerto):
    global tiempos_esperados
    
    llegada = env.now
    print ('esperando! %f' % llegada)

    with puerto.resource.request() as req:
        yield req

        #regitramos la espera
        espera = env.now - llegada
        print ('entrando %f' % env.now)
        #print ('llegada %f' % llegada)
        #print ('espera %f' % espera)
        tiempos_esperados.append(espera)

        terminal = puerto.get_terminal()

        tiempo_work = terminal.calcular_tiempo_buque(tipo_buque)
        print('tiempo word %f' %tiempo_work)

        #volvemos insertar terminal
        puerto.add_terminal(terminal)

        #hace el trabajo 
        yield env.timeout(tiempo_work)

        print ('saliendo %f' % env.now)


###############################################################################

print('Ejercicio 5 \n')

env = simpy.Environment()

puerto = Puerto(env, NUMERO_TERMINALES)

#print( len(puerto.terminales) )

env.process(generator(env, puerto))

env.run(until=TIEMPO_SIMULACION)


# Por ultimo se imprimen los datos pertinentes
#print ('d %f' % tiempos_esperados[0])

print('a) El tiempo de espera promedio fue: %f'
      % (sum(tiempos_esperados) / len(tiempos_esperados)))

print('b) El numero de tanques en el puerto fue: %f'
      % puerto.calcular_buques_servidos())

print('c)')
puerto.terminales.sort(key=attrgetter('nombre'), reverse=False)
for terminal in puerto.terminales:
    print('   Terminal %s estuvo desocupada el %.0f%% del tiempo total' %
          (terminal.nombre, 100 -
           (terminal.tiempo_trabajado * 100 / TIEMPO_SIMULACION)))