import simpy

def car(env):
     while True:
         print('Start parking at %d ' % env.now)
         parking_duration = 5
         yield env.timeout(parking_duration)

         print('Start driving at %d ' % env.now)
         trip_duration = 2
         yield env.timeout(trip_duration)

#################################################
print("Corriendo la simulacion")

env = simpy.Environment() #se inicializa en environment donde se corre todo

env.process(car(env)) # se indica cual es la funcion generetor 
                      # produce un iterador

env.run(until=15) #hasta cuando se corre