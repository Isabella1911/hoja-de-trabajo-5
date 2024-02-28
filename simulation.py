import simpy
import random

# Parámetros de la simulación
RANDOM_SEED = 42
MEMORIA_RAM = 100
CPU_SPEED = 3  # Número de instrucciones que el CPU puede procesar por unidad de tiempo
intervaloO_CREACION = 10  # intervaloo para la creación de procesos
SIM_TIME = 100  # Tiempo total de simulación

random.seed(RANDOM_SEED)  # Semilla para generar la misma secuencia de números aleatorios

class system:
    def __init__(self, env):
        self.RAM = simpy.Container(env, init=MEMORIA_RAM, capacity=MEMORIA_RAM)
        self.CPU = simpy.Resource(env, capacity=1)
        self.env = env

    def proceso(self, nombre, memoria_necesaria, instrucciones):
        yield self.env.timeout(random.expovariate(1.0 / intervaloO_CREACION))
        print(f'{env.now:.2f} - El proceso {nombre} ha llegado: necesita {memoria_necesaria} memoria, {instrucciones} instrucciones')

        # Estado NEW, solicita memoria RAM
        with self.RAM.get(memoria_necesaria) as req:
            yield req
            print(f'{env.now:.2f} - El proceso {nombre} ha pasado al estado READY')

            # Estado READY, espera por el CPU
            with self.CPU.request() as req_cpu:
                yield req_cpu
                while instrucciones > 0:
                    print(f'{env.now:.2f} - El proceso {nombre} está RUNNING')
                    yield self.env.timeout(1)  # Simula el tiempo de ejecución en el CPU

                    # Simula la ejecución de instrucciones
                    ejecutadas = min(instrucciones, CPU_SPEED)
                    instrucciones -= ejecutadas
                    print(f'{env.now:.2f} - El proceso {nombre} ha ejecutado {ejecutadas} instrucciones. Restan {instrucciones}')

                    if instrucciones <= 0:
                        print(f'{env.now:.2f} - El proceso {nombre} ha TERMINATED')
                        break
                    else:
                        evento = random.randint(1, 21)
                        if evento == 1:
                            print(f'{env.now:.2f} - El proceso {nombre} está WAITING por I/O')
                            yield self.env.timeout(2)  # Simula tiempo de espera por I/O
                        # El proceso siempre regresa a READY después de WAITING o continúa si no entra en WAITING

            self.RAM.put(memoria_necesaria)
            print(f'{env.now:.2f} - El proceso {nombre} ha liberado {memoria_necesaria} de memoria RAM')

def setup(env):
    sistema_operativo = system(env)

    for i in range(5):  # Inicia con 5 procesos
        env.process(sistema_operativo.proceso(f'Proceso {i}', random.randint(1, 10), random.randint(1, 10)))

    while True:
        yield env.timeout(random.expovariate(1.0 / intervaloO_CREACION))
        i += 1
        env.process(sistema_operativo.proceso(f'Proceso {i}', random.randint(1, 10), random.randint(1, 10)))

# Setup y ejecución de la simulación

env.process(setup(env))
env.run(until=SIM_TIME)
print("Procesador Empieza")
random.seed(RANDOM_SEED)
env = simpy.Environment()

procesador = simpy.Resource(env, capacity=1)
env.process(source(env, Procesos_Nuevos, Procesos_entre_intervaloos, procesador))
env.run()

media = sum(tiempos_finalizacion) / len(tiempos_finalizacion)
print("Media de los tiempos de finalización:", media)

diferencias_cuadradas = [(tiempo - media) ** 2 for tiempo in tiempos_finalizacion]
media_cuadrados_diferencias = sum(diferencias_cuadradas) / len(diferencias_cuadradas)
desviacion_estandar = math.sqrt(media_cuadrados_diferencias)

print("Desviación estándar de los tiempos de finalización:", desviacion_estandar)
