"""
Proyecto 01 Ejercicio 02

"""
import random
import simpy
from operator import attrgetter

""" Clase representante de un cajero """


class Cajero():

    def __init__(self, numero, env):
        self.numero = numero
        self.nombre = "Cajero %02d" % numero
        self.tiempo_trabajado = 0
        self.resource = simpy.Resource(env)


""" Constantes de programa """
RANDOM_SEED       = 42      # La libreria de random requiere un seed
TIEMPO_SIMULACION = 120     # La simulacion dura 120 minutos

NUMERO_CAJEROS      = 4     # Existen cuatro cajeros en el banco
CLIENTES_MINUTO     = 1     # Se genera un cliente nuevo por minuto
TIEMPO_SERVICIO_MIN = 3     # El minimo tiempo de servicio es tres minutos
TIEMPO_SERVICIO_MAX = 5     # El maximo tiempo de servicio es cinco minutos


""" Variables para clientes """
total_clientes     = 0      # Cuenta total de clientes que recibe la simulacion
tiempos_esperados  = []     # Tiempos esperados por cliente
clientes_atendidos = 0      # Cuenta el total de clientes atendidos
clientes_declinan  = 0      # Cuenta el total de clientes que declinan

""" Variables para cajeros """


def cajero_menor_cola(cajeros):
    """Dado el arreglo de cajeros retorna el cajero con la menor cola"""
    tamano_cola = 100000
    numero_cajero = 0
    i = 0
    for temp in cajeros:
        if len(temp.resource.queue) < tamano_cola:
            tamano_cola = len(temp.resource.queue)
            numero_cajero = i
        i += 1

    return cajeros[numero_cajero]


def numero_cajero_menor_cola(cajeros):
    """Dado el arreglo de cajeros retorna el numero del cajero con
       la menor cola"""

    tamano_cola = 100000
    numero_cajero = 0
    i = 0
    for temp in cajeros:
        if len(temp.resource.queue) < tamano_cola:
            tamano_cola = len(temp.resource.queue)
            numero_cajero = i
        i += 1

    return numero_cajero


def clienteDeclina(cajeros):
    """Dado el numero de clientes en cola determina si el cliente se queda
       o se va"""

    tamano_cola = len(cajero_menor_cola(cajeros).resource.queue)

    aleatorio = random.randint(0, 100)
    cota = 0
    if 6 <= tamano_cola <= 8:
        cota = 20
    elif 9 <= tamano_cola <= 10:
        cota = 40
    elif 11 <= tamano_cola <= 14:
        cota = 60
    elif 15 <= tamano_cola:
        cota = 80

    return aleatorio <= cota


def generador(env, clientes_minuto, cajeros):
    """Este proceso genera clientes al azar durante el tiempo
       de la simulacion"""
    global total_clientes, total_tiempo
    # Esta variabla actuara de contador de clientes
    cliente_actual = 1

    while True:
        # Se crea un nuevo cliente y se procesa
        c = cliente(env, ('Cliente %02d' % cliente_actual), cajeros)
        env.process(c)

        # Se saca un numero aleatorio siguiendo una distribucion exponencial
        t = random.expovariate(1.0 / clientes_minuto)

        # Esperamos t minutos para introducir el cliente c al sistema
        yield env.timeout(t)

        # Se actualizan las variables de estado de la simulacion
        total_clientes += 1
        cliente_actual += 1


def cliente(env, nombre_cliente, cajeros):
    """El cliente llegara al banco, si se queda esperar su turno y
       luego de ser atendido se ira"""
    global cajeros_libres, clientes_atendidos
    global clientes_declinan, tiempos_esperados, TIEMPO_SERVICIO_MIN
    global TIEMPO_SERVICIO_MAX, TIEMPO_SIMULACION

    # Se guarda el tiempo de llegada
    llegada = env.now

    # Se chequea si el cliente declinara dado el estado de la cola
    if clienteDeclina(cajeros):
        clientes_declinan += 1
        return

    # Aqui pedimos el recurso de cajeros al enviroment
    cajero_elegido = cajero_menor_cola(cajeros)
    with cajero_elegido.resource.request() as req:
        yield req

        # Chequeamos que no haya pasado el tiempo de la simulacion
        if env.now >= TIEMPO_SIMULACION:
            return

        # Guardamos el tiempo de espera de cliente y lo agregamos a la
        # lista de tiempos esperados
        espera = env.now - llegada
        tiempos_esperados.append(espera)

        # Luego generamos en tiempo de atencion por parte del cajero usando la
        # distribucion uniforme
        tiempo_atencion = random.uniform(
            TIEMPO_SERVICIO_MIN, TIEMPO_SERVICIO_MAX)
        yield env.timeout(tiempo_atencion)

        # Se actualiza el tiempo de trabajo para el cajero y se devuelve a la
        # lista
        cajero_elegido.tiempo_trabajado += tiempo_atencion

        # Se actualizan las variables de estado de la simulacion
        clientes_atendidos += 1

# Preparamos y comenzamos la simulacion
print('Ejercicio 02')
print('\n')
# random.seed(RANDOM_SEED)
env = simpy.Environment()

# Declaramos un nuevo recursos que representa los N cajeros
# Esta cola mantendra los cajeros libres a lo largo de la ejecucion
cajeros = [
    Cajero(1, env), Cajero(2, env), Cajero(3, env), Cajero(4, env)]

# Procesamos el generador de clientes y corremos la simulacion
env.process(generador(env, CLIENTES_MINUTO, cajeros))
env.run(until=TIEMPO_SIMULACION)

# Por ultimo se imprimen los datos pertinentes
print('a) El tiempo de espera promedio fue: %f'
      % (sum(tiempos_esperados) / len(tiempos_esperados)))
print('b) El porcentaje de clientes que declinaron es: %.0f%%'
      % (clientes_declinan * 100 / total_clientes))
print('c)')
for cajero in cajeros:
    print('   El porcentaje de tiempo desocupado de el %s fue: %.0f%%' %
          (cajero.nombre,
           100 - (cajero.tiempo_trabajado * 100 / TIEMPO_SIMULACION)))
