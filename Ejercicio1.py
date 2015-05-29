
import random
import simpy
from operator import attrgetter

""" Clase que representa un cajero """

class Cajero():

    def __init__(self, numero):
        self.numero = numero
        self.nombre = "Cajero %02d" % numero
        self.tiempo_trabajado = 0


""" Constantes de programa """
RANDOM_SEED       = 42      # La libreria de random requiere un seed
TIEMPO_SIMULACION = 480     # La simulacion dura 480 minutos

NUMERO_CAJEROS      = 4     # Existen cuatro cajeros en el banco
CLIENTES_MINUTO     = 1     # Se genera un cliente nuevo por minuto (60 por hora! 60/60 = 1 por min)
TIEMPO_SERVICIO_MIN = 3     # El minimo tiempo de servicio es tres minutos
TIEMPO_SERVICIO_MAX = 5     # El maximo tiempo de servicio es cinco minutos

""" Variables para clientes """
total_clientes     = 0      # Cuenta total de clientes que recibe la simulacion
tiempos_esperados  = []     # Tiempos esperados por cliente
clientes_encolados = 0      # Cuenta el total de clientes en cola
clientes_atendidos = 0      # Cuenta el total de clientes atendidos
clientes_declinan  = 0      # Cuenta el total de clientes que declinan

""" Variables para cajeros """
# Cola que tiene los cajeros libres
cajeros_libres = [Cajero(1), Cajero(2), Cajero(3), Cajero(4)]


def Declinar():
    global clientes_encolados

    aleatorio = random.randint(0, 100)
    cota = 0
    if 6 <= clientes_encolados <= 8:
        cota = 20
    elif 9 <= clientes_encolados <= 10:
        cota = 40
    elif 11 <= clientes_encolados <= 14:
        cota = 60
    elif 15 <= clientes_encolados:
        cota = 80

    return aleatorio <= cota


def generador(env, clientes_minuto, cajeros):
    """Generar Clientes de forma alazar"""
    global total_clientes, total_tiempo
    
    cliente_actual = 1      # Esta variabla actuara de contador de clientes

    while True:
        # Se crea un nuevo cliente y se procesa
        env.process(cliente(env, ('Cliente %02d' % cliente_actual), cajeros))

        # Se saca un numero aleatorio siguiendo una distribucion exponencial
        t = random.expovariate(1.0 / clientes_minuto)

        # Esperamos t para introducir un nuevo cliente. 
        yield env.timeout(t)

        # Actualizar variables
        total_clientes += 1
        cliente_actual += 1


def cliente(env, nombre_cliente, cajeros):

    global cajeros_libres, clientes_encolados, clientes_atendidos
    global clientes_declinan, tiempos_esperados, TIEMPO_SERVICIO_MIN
    global TIEMPO_SERVICIO_MAX, TIEMPO_SIMULACION

    # Se guarda el tiempo de llegada
    llegada = env.now

    # Revisamos el el cliente se queda o no. 
    if Declinar():
        clientes_declinan += 1
        return
    else:
        clientes_encolados += 1

    # Pedir recursos de cajero
    with cajeros.request() as req:
        yield req

        # Obtener algun cajero libre
        cajero_activo = cajeros_libres.pop(0)

        # Calcular cuanto espero por el cajero
        espera = env.now - llegada

        # Agregamos cuanto espero el cliente 
        tiempos_esperados.append(espera)
        
        # Tiempo que tarda en atender.
        tiempo_atencion = random.uniform(TIEMPO_SERVICIO_MIN, TIEMPO_SERVICIO_MAX)

        # Revisar si la simulacion termino o no para agregarlo a la lista de
        # cajeros libres
        if (env.now + tiempo_atencion >= TIEMPO_SIMULACION):
            cajeros_libres.append(cajero_activo)
            
        yield env.timeout(tiempo_atencion)

        # Actualizamos tiempo de cajero y agregamos a libres
        cajero_activo.tiempo_trabajado += tiempo_atencion
        cajeros_libres.append(cajero_activo)

        # Actualizamos variables
        clientes_encolados -= 1
        clientes_atendidos += 1


#####################################################################
""" El programa Main """
print('Ejercicio 01 \n')

#####################################################################
env = simpy.Environment()

cajeros = simpy.Resource(env, capacity=NUMERO_CAJEROS)

env.process(generador(env, CLIENTES_MINUTO, cajeros))

env.run(until=TIEMPO_SIMULACION)

#####################################################################
# Imprimimo datos 
print('a) El tiempo de espera promedio fue: %f'
      % (sum(tiempos_esperados) / len(tiempos_esperados)))
print('b) El porcentaje de clientes que declinaron es: %.0f%%'
      % (clientes_declinan * 100 / total_clientes))
print('c)')

# Se ordena la lista de cajeros por razones esteticas
cajeros_libres.sort(key=attrgetter('numero'), reverse=False)
for cajero in cajeros_libres:
    print('   El porcentaje de tiempo desocupado de el %s fue: %.0f%%' %
          (cajero.nombre,
           100 - (cajero.tiempo_trabajado * 100 / TIEMPO_SIMULACION)))
