import random
import simpy
import math

""" Clase representante de un cajero """
class Centro():

    def __init__(self, letra):
        self.letra = letra
        self.ocupado = 0
        self.nombre = "Centro %s" % letra
        self.tiempo_trabajado = 0

""" Constantes de programa """
RANDOM_SEED       = 42           
TIEMPO_SIMULACION = 120     # La simulacion dura 120 minutos

CLIENTES_HORA         = 5   # Se genera un cliente nuevo por hora
TIEMPO_SERVICIO_A_MIN = 6   # El minimo tiempo de servicio del centro A es seis minutos
TIEMPO_SERVICIO_A_MAX = 10  # El maximo tiempo de servicio del centro A es 10 minutos

""" Variables para clientes """
# Esta variable contara el total de clientes recibidos durante la simulacion
total_trabajos = 0

# Esta variable registrara los tiempos esperados de culminacion de un trabajo
tiempos_parados = []

# Esta variable contara el total de clientes en cola para el centro A
clientes_encolados_a = 0

# Esta variable contara el total de clientes en cola para el centro B
clientes_encolados_b = 0

# Esta variable contara el total de tiempos atendidos durante la simulacion
tiempos_totales = []

""" Variables para centros """
# Los dos centro de trabajo para la simulacion
centro_a = Centro('A')
centro_b = Centro('B')

def funcion_a_trozos(x):
    if (1<= x <= 3):
        return (1 / 4) * (x - 1)
    elif (3 < x <= 5):
        return (1 / 4) * (5 - x)
    else:
        return 0

def generador(env, clientes_hora, centros):
    global total_trabajos, total_tiempo

    cliente_actual = 1

    while True:
        # Se crea un nuevo cliente y se procesa
        c = cliente_centro_a(env, ('Cliente %02d' % cliente_actual), centros)
        env.process(c)

        # Se saca un numero aleatorio siguiendo una distribucion exponencial
        t = random.expovariate(CLIENTES_HORA)

        # Esperamos t minutos para introducir el cliente c al sistema
        yield env.timeout(t)

        # Se actualizan las variables de estado de la simulacion
        total_trabajos += 1
        cliente_actual += 1

def cliente_centro_a(env, nombre_cliente, centros):
    """El cliente llega al centro A y es atendido"""
    global centro_a, clientes_encolados_a, clientes_encolados_b
    global clientes_atendidos
    global tiempos_parados, TIEMPO_SERVICIO_A_MIN
    global TIEMPO_SERVICIO_A_MAX, TIEMPO_SIMULACION

    # Se guarda el tiempo de llegada
    llegada = env.now

    # Se chequea si el cliente declinara dado el estado de la cola
    clientes_encolados_a += 1

    # Aqui pedimos el recurso de cajeros al enviroment
    with centros[0].request() as req:
        yield req

        # Colocamos el centro a como ocupado
        centro_a.ocupado = 1

        # Luego generamos en tiempo de atencion por parte del centro A por Uniforme
        tiempo_atencion = random.uniform(
            TIEMPO_SERVICIO_A_MIN, TIEMPO_SERVICIO_A_MAX)

        if (env.now + tiempo_atencion >= TIEMPO_SIMULACION):
            centro_a.ocupado = 0
        yield env.timeout(tiempo_atencion)

        # Se actualiza el tiempo de trabajo para el cajero y se devuelve a la
        # lista
        centro_a.tiempo_trabajado += tiempo_atencion
        centro_a.ocupado = 0

        # Se actualizan las variables de estado de la simulacion
        clientes_encolados_a -= 1

        # Se pasa el trabajo a centro B si hay espacio en la cola,
        # sino se para el trabajo
        if (clientes_encolados_b < 4):
            env.process(cliente_centro_b(env, nombre_cliente, centros, llegada))
        else:
            espera = env.now
            while True:
                if (clientes_encolados_b < 4):
                    final = env.now - espera
                    tiempos_parados.append(final) 
                    env.process(cliente_centro_b(env, nombre_cliente, centros, llegada))
                    break

def cliente_centro_b(env, nombre_cliente, centros, llegada):
    """El cliente llega al centro B y es atendido, luego se va del sistema"""
    global centro_b, clientes_encolados_b, clientes_atendidos
    global TIEMPO_SIMULACION

    # Se chequea si el cliente declinara dado el estado de la cola
    clientes_encolados_b += 1

    # Aqui pedimos el recurso de cajeros al enviroment
    with centros[1].request() as req:
        yield req

        # Colocamos el centro a como ocupado
        centro_b.ocupado = 1

        # Luego generamos en tiempo de atencion por parte del centro B por
        # la funcion a trozos
        x = random.uniform(1,5) 
        tiempo_atencion = funcion_a_trozos(x) #ERROR!!!!!

        if (env.now + tiempo_atencion >= TIEMPO_SIMULACION):
            centro_b.ocupado = 0
        yield env.timeout(tiempo_atencion)

        # Se actualiza el tiempo de trabajo para el cajero y se devuelve a la
        # lista
        centro_b.tiempo_trabajado += tiempo_atencion
        centro_b.ocupado = 0

        # Se actualizan las variables de estado de la simulacion
        clientes_encolados_b -= 1
        final = env.now - llegada
        tiempos_totales.append(final)


#########################################################################################
print('Ejercicio 9')

env = simpy.Environment()

# Declaramos un nuevo recursos que representa los N cajeros
centro_a_resource = simpy.Resource(env, capacity = 1)
centro_b_resource = simpy.Resource(env, capacity = 1)
centros = [centro_a_resource, centro_b_resource]

# Procesamos el generador de clientes y corremos la simulacion
env.process(generador(env, CLIENTES_HORA, centros))
env.run(until=TIEMPO_SIMULACION)

# Por ultimo se imprimen los datos pertinentes
print('a) El numero de trabajos en el taller fue: %d'
      % (total_trabajos))
if (len(tiempos_parados) == 0):
    print('b) El porcentaje de veces que se para el centro A fue: 0%')
else:
    print('b) El porcentaje de veces que se para el centro A fue: %.0f%%'
          % (sum(tiempos_parados) * 100 / len(tiempos_parados)))
if (len(tiempos_totales) == 0):
    print('c) Tiempos de espera de culminacion de un trabajo fue 0 min')
else:
    print('c) Tiempos de espera de culminacion de un trabajo fue %.0f min'
          % (sum(tiempos_totales) / len(tiempos_totales)))