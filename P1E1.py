
import random
import simpy
from operator import attrgetter

""" Clase que representa un cajero cajero """


class Cajero():

    def __init__(self, numero):
        self.numero = numero
        self.nombre = "Cajero %02d" % numero
        self.tiempo_trabajado = 0


""" Constantes de programa """
RANDOM_SEED       = 42      # La libreria de random requiere un seed
TIEMPO_SIMULACION = 480     # La simulacion dura 480 minutos

NUMERO_CAJEROS      = 4     # Existen cuatro cajeros en el banco
CLIENTES_MINUTO     = 1     # Se genera un cliente nuevo por minuto
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
    """Determinar si el ciente declina o no"""
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
    global cajeros_libres, clientes_encolados, clientes_atendidos
    global clientes_declinan, tiempos_esperados, TIEMPO_SERVICIO_MIN
    global TIEMPO_SERVICIO_MAX, TIEMPO_SIMULACION

    # Se guarda el tiempo de llegada
    llegada = env.now

    # Se chequea si el cliente declinara dado el estado de la cola
    if Declinar():
        clientes_declinan += 1
        return
    else:
        clientes_encolados += 1

    # Aqui pedimos el recurso de cajeros al enviroment
    with cajeros.request() as req:
        yield req

        # Una vez que tenemos un cajero lo sacamos de la pila de cajeros libres
        cajero_activo = cajeros_libres.pop(0)

        # Luego guardamos el tiempo de espera de cliente y lo agregamos a la
        # lista de tiempos esperados
        espera = env.now - llegada
        
        # Luego generamos en tiempo de atencion por parte del cajero usando la
        # distribucion uniforme
        tiempo_atencion = random.uniform(
            TIEMPO_SERVICIO_MIN, TIEMPO_SERVICIO_MAX)
        # Es importante revisar si el tiempo de atencion tomara mas que el
        # tiempo restante de simulacion de forma que el cajero sea devuelto a
        # la lista antes de salir de la simulacion
        if (env.now + tiempo_atencion >= TIEMPO_SIMULACION):
            cajeros_libres.append(cajero_activo)
        yield env.timeout(tiempo_atencion)

        tiempos_esperados.append(espera)

        # Se actualiza el tiempo de trabajo para el cajero y se devuelve a la
        # lista
        cajero_activo.tiempo_trabajado += tiempo_atencion
        cajeros_libres.append(cajero_activo)

        # Se actualizan las variables de estado de la simulacion
        clientes_encolados -= 1
        clientes_atendidos += 1


""" El programa Main """
print('Ejercicio 01')
print('\n')

env = simpy.Environment()

# Declaramos un nuevo recursos que representa los N cajeros
cajeros = simpy.Resource(env, capacity=NUMERO_CAJEROS)

# Procesamos el generador de clientes y corremos la simulacion
env.process(generador(env, CLIENTES_MINUTO, cajeros))
env.run(until=TIEMPO_SIMULACION)

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
