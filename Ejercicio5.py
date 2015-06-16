import random
import simpy
import math
from operator import attrgetter

""" Constantes de programa """
RANDOM_SEED       = 42      
TIEMPO_SIMULACION = 30    	# un a~o de simulacion

NUMERO_TERMINALES = 2 		# Existen N terminales en el puerto
EXTRA = 5

tiempos_esperados = []

""" VAraibles para las n-esimas simulacinoes"""
SIMULATION            = 10000 
TOTAL_TIEMPO_PROMEDIO = []
TOTAL_BUQUES_SERVIDOS = []

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

    def overflow(self, time):
        self.tiempo_trabajado -= time

    def calcular_tiempo_buque(self, tipo_buque):
        tiempo_trabajado = 0

        if self.nombre == 'A':
            if tipo_buque == 'G':
                tiempo_trabajado = 4 + EXTRA
                self.tiempo_trabajado += 4 + EXTRA
                self.buques_G_servidos += 1
                return tiempo_trabajado
            elif tipo_buque == 'M':
                tiempo_trabajado = 3 + EXTRA
                self.tiempo_trabajado += 3 + EXTRA
                self.buques_M_servidos += 1
                return tiempo_trabajado
            elif tipo_buque == 'P':
                tiempo_trabajado = 2 + EXTRA
                self.tiempo_trabajado += 2 + EXTRA
                self.buques_P_servidos += 1
                return tiempo_trabajado
        elif self.nombre == 'B':
            if tipo_buque == 'G':
                tiempo_trabajado = 3 + EXTRA
                self.tiempo_trabajado += 3 + EXTRA
                self.buques_G_servidos += 1
                return tiempo_trabajado
            elif tipo_buque == 'M':
                tiempo_trabajado = 2 + EXTRA
                self.tiempo_trabajado += 2 + EXTRA
                self.buques_M_servidos += 1
                return tiempo_trabajado
            elif tipo_buque == 'P':
                tiempo_trabajado = 1 + EXTRA
                self.tiempo_trabajado += 1 + EXTRA
                self.buques_P_servidos += 1
                return tiempo_trabajado

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
        #print('tipo %s' %type_buque)
        dias       = tiempo_llegada()  #dias que tarda en llegar
        #print('dias1 %f' %dias)

        yield env.timeout(dias) 

        env.process(buque(env, ('Buque %02d' % contador_buques), 
                          type_buque, puerto) )        

        #yield env.timeout(dias) #muevo el tiempo unidad: dias

        contador_buques += 1
        #print('next buque')

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

        if (env.now + tiempo_work >= TIEMPO_SIMULACION):
            # si me paso no debo considerar el tiempo
            terminal.overflow(tiempo_work) 

        #volvemos insertar terminal
        puerto.add_terminal(terminal)

        #hace el trabajo 
        yield env.timeout(tiempo_work)

        print ('saliendo %f' % env.now)

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

###############################################################################

print('Ejercicio 5 \n')

for x in range(0,100):
    #Reset de la variables
    tiempos_esperados = []

    #Comienza simulacion
    env = simpy.Environment()

    puerto = Puerto(env, NUMERO_TERMINALES)

    #print( len(puerto.terminales) )

    env.process(generator(env, puerto))

    env.run(until=TIEMPO_SIMULACION)

    # Por ultimo se imprimen los datos
    if (0 <= x <= 5):
        print('a) El tiempo de espera promedio fue: %f dias'
              % (sum(tiempos_esperados) / len(tiempos_esperados)))

        print('b) El numero de tanques en el puerto fue: %f'
              % puerto.calcular_buques_servidos())

        print('c)')
        puerto.terminales.sort(key=attrgetter('nombre'), reverse=False)
        for terminal in puerto.terminales:
            print('   Terminal %s estuvo desocupada el %.0f%% del tiempo total' %
                  (terminal.nombre, 100 -
                   (terminal.tiempo_trabajado * 100 / TIEMPO_SIMULACION)))
            print('time %f' % terminal.tiempo_trabajado)

    #Agregar a arreglos
    TOTAL_TIEMPO_PROMEDIO.append(sum(tiempos_esperados) / len(tiempos_esperados))
    TOTAL_BUQUES_SERVIDOS.append(puerto.calcular_buques_servidos())

######################
print('ESTADISTICAS \n\n')

mean  = media(TOTAL_TIEMPO_PROMEDIO)
mean1 = media(TOTAL_BUQUES_SERVIDOS)
# mean1      = media(TOTAL_DECLINADOS)

print "La media del total de tiempo promedio fue"
print mean, "dias"
print ('\n')
print "La media del total de buques atendidos fue"
print mean1

##########
desviation  = desv(TOTAL_TIEMPO_PROMEDIO)
desviation1 = desv(TOTAL_BUQUES_SERVIDOS)
print ('\n')
print "La desviacion del total de tiempo promedio fue"
print desviation, "dias"
print ('\n')
print "La desviacion del total de buques atendidos fue"
print desviation1
print ('\n')

#############
interval   = intervalo(TOTAL_TIEMPO_PROMEDIO)
interval1  = intervalo(TOTAL_BUQUES_SERVIDOS)

print "El intervalo de confianza del total de tiempo promedio fue"
print interval, "dias"
print ('\n')
print "El intervalo de confianza del total de buques atendidos fue"
print interval1