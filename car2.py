import simpy

# env el enviroment
# name el nombre del carro
# bsc es donde se recarga la bateria 
# driving time es cuanto tarda en llegar a la estacion
# charge duration es cuanto tarda en cargar
def car(env, name, bcs, driving_time, charge_duration):
     # Simulate driving to the BCS
     yield env.timeout(driving_time)

     # Request one of its charging spots
     print('%s arriving at %d' % (name, env.now))
     with bcs.request() as req:
         yield req

         # Charge the battery
         print('%s starting to charge at %s' % (name, env.now))
         yield env.timeout(charge_duration) #espera el evento
         print('%s leaving the bcs at %s' % (name, env.now))

#################################################
print('Comenzando simulacion \n')

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2) # es un recurso y dices su capacidad
for i in range(4):
     env.process(car(env, 'Car %d' % i, bcs, i*2, 5))
env.run()