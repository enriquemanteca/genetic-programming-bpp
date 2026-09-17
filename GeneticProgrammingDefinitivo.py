import math
import Util
import random
import time
import numpy as np

from Util import *

# Parámetros PG
profundidad_maxima = 5
constantes = [0.25, 0.50, 0.75]
terminales = ["sap", "obj_size", "remaining","dif_obj_avg"]
hojas = ["0.25", "0.50", "0.75", "sap", "obj_size", "remaining","dif_obj_avg"]
binarias = ["+", "-","*","/"]
unarias = ["neg"]

# Constructor de planificaciones
def schedule_builder(instance, arbol):
    num_objects = instance.dimension
    objects = instance.objects
    placed = [False] * num_objects
    display = np.zeros(num_objects)
    bin_capacity= instance.capacity

    current_object = 0
    placed[current_object] = True
    display[current_object]=1
    current_bin_capacity=bin_capacity-objects[current_object]
    total_bins = 1
    objetos_por_colocar=num_objects-1
    for _ in range(num_objects - 1):
        max_priority = -float('inf')
        best_object = None


        for object in range(num_objects):
            if not placed[object] and objects[object]<=current_bin_capacity:
                # Espacio que quedaría en el contenedor después de poner el objeto
                sap = current_bin_capacity-objects[object]
                #Tamaño del objeto actual
                obj_size = objects[object]
                # Suma de tamaños restantes
                remaining = sum([objects[i] for i in range(num_objects) if not placed[i]])
                dif_obj_avg=abs(obj_size-remaining/objetos_por_colocar)
                domain = DomainInfo(sap, obj_size, remaining,dif_obj_avg)
                priority = arbol.evaluar(domain)
                if priority > max_priority:
                    max_priority = priority
                    best_object = object

        # Si ningún objeto cabe en el contenedor, best_object será None, si esto ocurre se abre un nuevo contenedor y se vuelve a buscar el mejor
        # Otra opción sería que solo se calculase el objeto más prioritario, si cabe se mete en ese contenedor, si no, se abre un nuevo contenedor
        if best_object==None:
            total_bins += 1
            current_bin_capacity=bin_capacity
            for object in range(num_objects):
                if not placed[object] and objects[object]<=current_bin_capacity:
                    # Espacio que quedaría en el contenedor después de poner el objeto
                    sap = current_bin_capacity-objects[object]
                    #Tamaño del objeto actual
                    obj_size = objects[object]
                    # Suma de tamaños restantes
                    remaining = sum([objects[i] for i in range(num_objects) if not placed[i]])
                    dif_obj_avg=abs(obj_size-remaining/objetos_por_colocar)
                    domain = DomainInfo(sap, obj_size, remaining,dif_obj_avg)
                    priority = arbol.evaluar(domain)
                    if priority > max_priority:
                        max_priority = priority
                        best_object = object

        current_bin_capacity=current_bin_capacity-objects[best_object]
        placed[best_object] = True
        display[best_object]=total_bins
        current_object = best_object
        objetos_por_colocar -= 1
    # Cerrar el ciclo de vuelta a la ciudad inicial
    # Crear un objeto solucion con la ruta y la distancia
    solution = BinPackingSolution(display)
    return solution

def schedule_builder_v2(instance, arbol):
    num_objects = instance.dimension
    objects = instance.objects
    placed = [False] * num_objects
    display = np.zeros(num_objects)
    bin_capacity= instance.capacity

    current_object = 0  # Starting from the first city
    placed[current_object] = True
    display[current_object]=1
    current_bin_capacity=bin_capacity-objects[current_object]
    total_bins = 1
    objetos_por_colocar=num_objects-1

    for _ in range(num_objects - 1):
        max_priority = -float('inf')
        best_object = None
        
        for object in range(num_objects):
            if not placed[object]:
                # Espacio que quedaría en el contenedor después de poner el objeto
                sap = current_bin_capacity-objects[object]
                #Tamaño del objeto actual
                obj_size = objects[object]
                # Suma de tamaños restantes
                remaining = sum([objects[i] for i in range(num_objects) if not placed[i]])
                dif_obj_avg=abs(obj_size-remaining/objetos_por_colocar)
                domain = DomainInfo(sap, obj_size, remaining,dif_obj_avg)
                priority = arbol.evaluar(domain)
                if priority > max_priority:
                    max_priority = priority
                    best_object = object

        if current_bin_capacity<objects[best_object]:
            total_bins += 1
            current_bin_capacity = bin_capacity


        current_bin_capacity=current_bin_capacity-objects[best_object]
        placed[best_object] = True
        display[best_object]=total_bins
        current_object = best_object
        objetos_por_colocar-=1
    # Cerrar el ciclo de vuelta a la ciudad inicial
    # Crear un objeto solucion con la ruta y la distancia
    solution = BinPackingSolution(display)
    return solution


    
def schedule_builder_v3(instance, arbol):
    num_objects = instance.dimension
    objects = instance.objects
    placed = [False] * num_objects
    display = np.zeros(num_objects)
    bin_capacity = instance.capacity

    # Contenedores disponibles, en lugar de solo uno
    bin_capacities = [bin_capacity]  # Lista de capacidades de contenedores abiertos
    current_object = 0  # Empezamos con el primer objeto
    placed[current_object] = True
    display[current_object] = 1
    bin_capacities[0] -= objects[current_object]  # Reducimos la capacidad del primer contenedor
    objetos_por_colocar=num_objects-1

    for _ in range(num_objects - 1):
        max_priority = -float('inf')
        best_object = None
        best_bin = None
        
        for object in range(num_objects):
            if not placed[object]:
                # Intentamos colocar el objeto en los contenedores abiertos
                best_local_priority = -float('inf')
                local_bin = None
                for i, remaining_capacity in enumerate(bin_capacities):
                    if remaining_capacity >= objects[object]:
                        # Espacio que quedaría en el contenedor después de poner el objeto
                        sap = remaining_capacity - objects[object]
                        # Tamaño del objeto actual
                        obj_size = objects[object]
                        # Suma de tamaños restantes
                        remaining = sum([objects[i] for i in range(num_objects) if not placed[i]])
                        dif_obj_avg=abs(obj_size-remaining/objetos_por_colocar)
                        domain = DomainInfo(sap, obj_size, remaining, dif_obj_avg)
                        priority = arbol.evaluar(domain)
                        if priority > best_local_priority:
                            best_local_priority = priority
                            local_bin = i
                
                if best_local_priority > max_priority:
                    max_priority = best_local_priority
                    best_object = object
                    best_bin = local_bin

        # Si el objeto no cabe en los contenedores existentes, agregamos uno nuevo
        if best_bin is None:
            for object in range(num_objects):
                sap = bin_capacity-objects[object]
                #Tamaño del objeto actual
                obj_size = objects[object]
                # Suma de tamaños restantes
                remaining = sum([objects[i] for i in range(num_objects) if not placed[i]])
                dif_obj_avg=abs(obj_size-remaining/objetos_por_colocar)
                domain = DomainInfo(sap, obj_size, remaining,dif_obj_avg)
                priority = arbol.evaluar(domain)
                if priority > max_priority:
                    max_priority = priority
                    best_object = object
            bin_capacities.append(bin_capacity - objects[best_object])
            total_bins = len(bin_capacities)  # Ahora el total de contenedores es el tamaño de la lista
            display[best_object] = total_bins
        else:
            bin_capacities[best_bin] -= objects[best_object]
            display[best_object] = best_bin + 1  # Los contenedores se numeran desde 1 en adelante

        placed[best_object] = True
        current_object = best_object
        objetos_por_colocar-=1
    # Crear la solución final
    solution = BinPackingSolution(display)
    return solution

# Función de evaluación
def train(instances, arbol, schedule=1):
    trainingValue = 0.0
    for instance in instances:
        if schedule ==2:
            trainingValue += schedule_builder_v2(instance, arbol).bins_used
        elif schedule ==3:
            trainingValue += schedule_builder_v3(instance, arbol).bins_used
        else:
            trainingValue += schedule_builder(instance, arbol).bins_used

    return trainingValue

# Programa Genético
def genetic_programming(instances, pop_size=1000, num_generations=50, mutation_rate=0.2, schedule=1, lsa_rate= 0.3,lsa_neighbours=5):
    ## generar y evaluar poblacion inicial
    population = generarPoblacionInicial(pop_size)
    population = evaluarPoblacion(population, instances,schedule)
    # Inicializamos la lista para guardar el bins_used del mejor individuo por generación
    traza=[]
    printGeneration(0,population)

    ## evolucionar num_generations poblaciones
    for g in range(1, num_generations):
        offspring = []
        i = 0
        while i < pop_size-2:
            parent1 = torneo(5, population)
            parent2 = torneo(5, population)
            if random.random() < 0.8:
                child1 = crossover(parent1, parent2)
                child2 = crossover(parent2, parent1)
                if random.random() < mutation_rate:
                    child1 = mutate(child1)
                if random.random() < mutation_rate:
                    child2 = mutate(child2)
                child1.bins_used = train(instances, child1,schedule)
                child2.bins_used = train(instances, child2,schedule) 
                if random.random() < lsa_rate:
                    child1 = lsa(child1, lsa_neighbours, instances,schedule)
                if random.random() < lsa_rate:
                    child2 = lsa(child2, lsa_neighbours, instances,schedule)  
                offspring.append(child1)
                offspring.append(child2)
            else:
                offspring.append(parent1)
                offspring.append(parent2)
            i = i + 2
        best = find_best_solution(population)
        offspring.append(best)
        offspring.append(best)
        population = offspring
        mejor = find_best_solution(population) # Seleccionamos el mejor individuo de la generación
        traza.append(mejor.bins_used)           # Guardamos su bins_used para trazar la convergencia
        printGeneration(g,population)

    ## devolver mejor individuo en la población final
    return find_best_solution(population), traza

def genetic_programming_v2(instances, pop_size=1000, num_generations=50, mutation_rate=0.2,  schedule=1, lsa_rate = 0.3, lsa_neighbours = 5):
    #    La diferencia entre este algoritmo de programación genética y el anterior es que en vez de hacer el torneo con los padres y luego cruzarlos,
    # se cruzan todos los padres de una generación para después hacer el torneo entre los padres y los hijos y elegir los 2 mejores. Tras elegir los 2 mejores se aplica
    # ls con una probabilidad
    ## generar y evaluar poblacion inicial
    population = generarPoblacionInicial(pop_size)
    population = evaluarPoblacion(population, instances, schedule)
    # Inicializamos la lista para guardar el bins_used del mejor individuo por generación
    traza=[]
    printGeneration(0,population)

    ## evolucionar num_generations poblaciones
    for g in range(1, num_generations):
        offspring = []
        i = 0
        random_sort_population(population)  # mezclar poblacion
        while i < pop_size:
            # selección incondicional de los padres por pares
            parent1 = population[i]
            parent2 = population[i + 1]
            # cruce incondicional
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            # mutación con probabilidad
            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)
            # calculo del fitness
            child1.bins_used = train(instances, child1,schedule)
            child2.bins_used = train(instances, child2,schedule) 
            # reemplazo con torneo
            tournament = []
            tournament.extend([parent1, parent2, child1, child2])
            tournament = sort_population(tournament)

			# lsa con probabilidad
            if random.random() < lsa_rate:
                tournament[0] = lsa(tournament[0], lsa_neighbours, instances,schedule)
            if random.random() < lsa_rate:
                tournament[1] = lsa(tournament[1], lsa_neighbours, instances,schedule)
            offspring.extend([tournament[0], tournament[1]])
            i = i + 2
        population = offspring
        mejor = find_best_solution(population) # Seleccionamos el mejor individuo de la generación
        traza.append(mejor.bins_used)           # Guardamos su bins_used para trazar la convergencia
        printGeneration(g,population)
    ## devolver mejor individuo en la población final
    return mejor, traza


def printGeneration(g, population):
    best = find_best_solution(population)
    print(g, best.bins_used, best.getRegla(), sep=" ")

def generarPoblacionInicial(pop_size):
    population = []
    for _ in range(pop_size):
        ind = Arbol(profundidad_maxima)
        ind.crearAleatorio()
        population.append(ind)
    return population

def evaluarPoblacion(population, instances, schedule):
    for i in range(len(population)):
        population[i].bins_used = train(instances, population[i], schedule)
    return population

def random_sort_population(population):
    return random.shuffle(population)

def find_best_solution(population):
    return min(population, key=lambda x: x.bins_used)

def sort_population(population):
    return sorted(population, key=lambda x: x.bins_used)

def torneo(torneo_size, population):
    tournament = []
    for g in range(0, torneo_size):
        tournament.append(population[random.randint(0, len(population)-1)])
    tournament = sort_population(tournament)
    return tournament[0]

def crossover(padre1, padre2):
    i, j, k = 0, 0, 0
    n = 1000

    while k < n:
        i = padre1.posAzar()
        j = padre2.posAzar()
        k += 1
        if j != -1:
            break

    if j == -1:
        r = Arbol(profundidad_maxima)
        r.crearAleatorio()
        return r

    hijo1 = Arbol(profundidad_maxima)
    hijo1.cruza(i, j, padre1, padre2)
    hijo2 = Arbol(profundidad_maxima)
    hijo2.cruza(j, i, padre2, padre1)

    if not hijo1.esValido():
        hijo1 = None
    if not hijo2.esValido():
        hijo2 = None

    if hijo1 is None and hijo2 is None:
        return Arbol(profundidad_maxima)
    elif hijo1 is not None and hijo2 is None:
        return hijo1
    elif hijo1 is None and hijo2 is not None:
        return hijo2
    else:
        return hijo1

def mutate(cromosoma):
    mutacion = Arbol(profundidad_maxima)
    mutacion.crearAleatorio()
    i, j, k = 0, 0, 0
    n = 1000

    while j != -1 and k < n:
        i = cromosoma.posAzar()
        j = mutacion.posAzar()
        k += 1

    if j == -1:
        return mutacion

    hijo = Arbol(profundidad_maxima)
    hijo.cruza(i, j, cromosoma, mutacion)

    if hijo.esValido():
        return hijo
    else:
        return mutacion

def lsa(cromosoma, lsa_neighbours, instances, schedule):
    # Para evitar que la búsqueda local sea muy costosa se pone un filtro para no tener que evaluarlo con todas las instancias
    # A parte del filtro hemos puesto que si el problema tiene mas de 5 instancias el numero de instancias usadas en la ls irá variando, así como las instancias usadas
    #  En caso de que tenga menos de 5 instancias solo se cogerá una para ls pero también irá variando
    filter = []
    if len(instances)>5:
        numero = random.randint(1, 2)
        k = random.sample(range(0, len(instances)), numero)
        for i in k:
            filter.append(instances[i])
    else:
        numero = random.randint(0, len(instances)-1)
        filter.append(instances[numero])
    # se generan lsa_neighbours y se evaluan con el filtro
    best = mutate(cromosoma)
    best.bins_usedFilter = train(filter, best, schedule)
    for g in range(1, lsa_neighbours):
        neighbour = mutate(cromosoma)
        neighbour.bins_usedFilter = train(filter, neighbour,schedule)
        if neighbour.bins_usedFilter < best.bins_usedFilter: 
            best = neighbour
    # el mejor se evalua con el train
    best.bins_used = train(instances, neighbour,schedule)
    if best.bins_used < cromosoma.bins_used:
            return best
    return cromosoma 

class Nodo:
    def __init__(self, valor):
        self.valor = valor

#Ampliamos la clase DomainInfo para incluir variables adicionales.
#El tamaño del objeto (obj_size) y la suma de los tamaños restantes (remaining).
class DomainInfo:
    def __init__(self, sap,obj_size,remaining,dif_obj_avg):
        self.sap = sap
        self.obj_size=obj_size
        self.remaining=remaining
        self.dif_obj_avg=dif_obj_avg

class Arbol:
    def __init__(self, profundidad_maxima):
        self.profundidad_maxima = profundidad_maxima
        self.sizeMax = int(math.pow(2, profundidad_maxima) - 1)
        self.nodos = [None] * self.sizeMax
        self.size = 0
        self.elementos = []
        self.regla = ""
        self.monticulo = ""
        self.bins_used = 0

    ## operador cruce del GP
    def cruza(self, posicionPadre1, posicionPadre2, padre1, padre2):
        self.nodos = padre1.nodos.copy()
        self.profundidad_maxima = padre1.profundidad_maxima
        self.sizeMax = int(math.pow(2, profundidad_maxima) - 1)
        self.size = padre1.size
        self.borrar(posicionPadre1)
        self.insertar(posicionPadre1, posicionPadre2, padre2)

    def insertar(self, i, j, arbol):
        if arbol.nodos[j] is not None:
            self.nodos[i] = Nodo(arbol.nodos[j].valor)
            self.size += 1
            if (2 * i + 1) < len(self.nodos) and (2 * j + 1) < len(arbol.nodos):
                self.insertar(2 * i + 1, 2 * j + 1, arbol)
            if (2 * i + 2) < len(self.nodos) and (2 * j + 2) < len(arbol.nodos):
                self.insertar(2 * i + 2, 2 * j + 2, arbol)

    def borrar(self, i):
        if self.nodos[i] is not None:
            self.size -= 1
            self.nodos[i] = None
            if (2 * i + 1) < len(self.nodos):
                self.borrar(2 * i + 1)
            if (2 * i + 2) < len(self.nodos):
                self.borrar(2 * i + 2)

    def posAzar(self):
        pos = [i for i in range(len(self.nodos)) if self.nodos[i] is not None]
        if pos:
            return random.choice(pos)
        return -1

    ## generar aleatorios
    def crearAleatorio(self):
        completo = random.choice([True, False])
        while not self.esValido():
            self.clear()
            if completo:
                self.generarCompleto()
            else:
                self.generarDegenerado()

    def clear(self):
        self.nodos = [None] * self.sizeMax
        self.size = 0

    def generarCompleto(self):
        for i in range(self.sizeMax - 1, -1, -1):
            if self.hoja(i):
                self.generaTerminalConstante(i)
                self.size += 1
            else:
                if self.nodos[2 * i + 1] is not None and self.nodos[2 * i + 2] is not None:
                    self.generaBinaria(i)
                self.size += 1

    def generarDegenerado(self):
        for i in range(self.sizeMax - 1, -1, -1):
            if self.hoja(i) or self.nodos[2 * i + 1] is None:
                if not self.hijoDerecho(i) and self.nodos[i + 1] is not None:
                    self.generaTerminalConstante(i)
                else:
                    self.generaHoja(i)
            else:
                if self.nodos[2 * i + 2] is not None:
                    self.generaBinaria(i)
                else:
                    self.generaUnaria(i)
            if self.nodos[i] is not None:
                self.size += 1
        if not self.esValido(): # si no se crease correctamente se vuelve a llamar al método
            self.clear()
            self.generarDegenerado()

    ## evaluación de la regla codificada en el árbol
    def evaluar(self, domain):
        rdo=self.evaluar_nodo(0, domain) 
        return rdo if rdo is not None else 0
#Ampliamos la función de evaluación para incluir las nuevas terminales.
    def evaluar_nodo(self, i, domain):
        if i >= len(self.nodos):
            return 0
        nodo = self.nodos[i]
        if nodo is not None:
            if nodo.valor == "sap":
                return domain.sap
            elif nodo.valor=="obj_size":
                return domain.obj_size
            elif nodo.valor=="remaining":
                return domain.remaining
            elif nodo.valor=="dif_obj_avg":
                return domain.dif_obj_avg
            elif nodo.valor == "neg":
                hijo=self.evaluar_nodo(2*i+1, domain)
                return -hijo if hijo is not None else 0
            elif nodo.valor == "+":
                izq=self.evaluar_nodo(2*i+1, domain)
                dcha=self.evaluar_nodo(2*i+2, domain)
                return (izq if izq is not None else 0) + (dcha if dcha is not None else 0)
 
            elif nodo.valor == "-":
                izq=self.evaluar_nodo(2*i+1, domain)
                dcha=self.evaluar_nodo(2*i+2, domain)
                return (izq if izq is not None else 0) - (dcha if dcha is not None else 0)
            elif nodo.valor == "*":
                return self.evaluar_nodo(2*i+1, domain) * self.evaluar_nodo(2*i+2, domain)
            elif nodo.valor == "/":
                derecha_valor = self.evaluar_nodo(2*i+2, domain)
                if derecha_valor != 0: # Evitar división por cero
                    return self.evaluar_nodo(2*i+1, domain) / derecha_valor
                else:
                    return 1
            else:
                    try:
                        return float(nodo.valor) # una constante númerica
                    
                    except:
                        return 0  # Devuelve 0 en lugar de None si el valor no es convertible
        
        else:
            return 0
            
    ## representar el árbol como una regla
    def getRegla(self):
        self.elementos = []
        self.calculaRepresentacion(0)
        self.regla = "".join(self.elementos)
        return self.regla

    def calculaRepresentacion(self, i):
        if self.nodos[i] is not None:
            if self.binaria(i):
                self.elementos.append("(")
                if (2 * i + 1) < len(self.nodos):
                    self.calculaRepresentacion(2 * i + 1)
                self.elementos.append(self.nodos[i].valor)
                if (2 * i + 2) < len(self.nodos):
                    self.calculaRepresentacion(2 * i + 2)
                self.elementos.append(")")
            elif self.unaria(i):
                self.elementos.append(self.nodos[i].valor)
                self.elementos.append("(")
                if (2 * i + 1) < len(self.nodos):
                    self.calculaRepresentacion(2 * i + 1)
                self.elementos.append(")")
            else:
                self.elementos.append(str(self.nodos[i].valor))

    ## representa en formato montículo
    def getMonticulo(self):
        list = []
        for i in range(0, self.sizeMax):
            if self.nodos[i] is None:
                list.append("NULL")
            else:
                list.append(str(self.nodos[i].valor))
        self.monticulo = " ".join(list)
        return self.monticulo
    
    def cargarMonticulo(self, s):
        simbolos = s.replace('\n', '').split(" ")
        list = []
        for i in range(0,len(simbolos)):
            if "0" in simbolos[i]:
                self.nodos[i] = Nodo(float(simbolos[i]))
                self.size += 1
            elif simbolos[i] != "NULL":                
                self.nodos[i] = Nodo(simbolos[i])
                self.size += 1
        self.monticulo = " ".join(list)	

    ## validar si el árbol es válido
    def esValido(self):
        if self.nodos[0] is None:
            return False
        for i in range(len(self.nodos)):
            if self.nodos[i] is not None:
                if self.hoja(i) and self.operacion(i):
                    return False
                if 2 * i + 1 < len(self.nodos):
                    if self.binaria(i) and (self.nodos[2 * i + 1] is None or self.nodos[2 * i + 2] is None): # binaria sin hijos
                        return False
                    if self.unaria(i) and self.nodos[2 * i + 1] is None: # unaria sin hijos
                        return False
                    if self.terminal(i) and (self.nodos[2 * i + 1] is not None or self.nodos[2 * i + 2] is not None):  # es terminal y tiene hijos
                        return False
                if i > 0:
                    if self.nodos[(i - 1) // 2] is None:  # padreNull
                        return False
                    if self.terminal((i - 1) // 2):  # padre terminal
                        return False
        return True

    ## auxiliares
    def hijoDerecho(self, i):
        return i % 2 == 0 and i != 0

    def hoja(self, i):
        return i >= len(self.nodos) // 2

    def terminal(self, i):
        return str(self.nodos[i].valor) in terminales

    def constante(self, i):
        return str(self.nodos[i].valor) in constantes

    def operacion(self, i):
        return self.binaria(i) or self.unaria(i)

    def binaria(self, i):
        return str(self.nodos[i].valor) in binarias

    def unaria(self, i):
        return str(self.nodos[i].valor) in unarias

    ## tocar estas funciones para alterar las probabilidades con las que se genera cada símbolo
    def generaHoja(self, i):
        random_num = random.randint(0, 50)
        if random_num < 3:
            self.nodos[i] = Nodo(random.choice(constantes))
        elif 3 <= random_num <= 5:
            self.nodos[i] = Nodo(random.choice(terminales))
        else:
            self.nodos[i] = None

    def generaTerminalConstante(self, i):
        random_num = random.randint(0, 5)
        if random_num < 3:
            self.nodos[i] = Nodo(random.choice(constantes))
        else:
            self.nodos[i] = Nodo(random.choice(terminales))

    def generaBinaria(self, i):
        self.nodos[i] = Nodo(random.choice(binarias))

    def generaUnaria(self, i):
        self.nodos[i] = Nodo(random.choice(unarias))

def load_rules(filename):
    reglas = []
    with open(filename, 'r') as archivo:
        lineas = archivo.readlines()
        for s in lineas:
            regla = Arbol(profundidad_maxima)
            regla.cargarMonticulo(s)
            reglas.append(regla)
    return reglas

def schedule_builder_sum(instance, ensemble):
    num_objects = instance.dimension
    objects = instance.objects
    placed = [False] * num_objects
    display = np.zeros(num_objects)
    bin_capacity= instance.capacity

    current_object = 0  # Starting from the first city
    placed[current_object] = True
    display[current_object]=1
    current_bin_capacity=bin_capacity-objects[current_object]
    total_bins = 1
    objetos_por_colocar=num_objects-1


    for _ in range(num_objects - 1):
        priorities = [0] * num_objects
        best_object = None

        for object in range(num_objects):
            for arbol in ensemble:
                if not placed[object]:
                    # Espacio que quedaría en el contenedor después de poner el objeto
                    sap = current_bin_capacity-objects[object]
                    #Tamaño del objeto actual
                    obj_size = objects[object]
                    # Suma de tamaños restantes
                    remaining = sum([objects[i] for i in range(num_objects) if not placed[i]])
                    dif_obj_avg=abs(obj_size-remaining/objetos_por_colocar)
                    domain = DomainInfo(sap, obj_size, remaining,dif_obj_avg)
                    priority = arbol.evaluar(domain)
                    priorities[object] += priority

        best_object = None
        max_priority = -float('inf')
        for object in range(num_objects):
            if not placed[object]:
                priority = priorities[object]
                if priority > max_priority:
                    max_priority = priority
                    best_object = object


        if current_bin_capacity<objects[best_object]:
            total_bins += 1
            current_bin_capacity = bin_capacity


        current_bin_capacity=current_bin_capacity-objects[best_object]
        placed[best_object] = True
        display[best_object]=total_bins
        current_object = best_object
        objetos_por_colocar-=1
    solution = BinPackingSolution(display)
    return solution

def generarEnsembleAleatorio(n, reglas):
    ensemble = []
    for i in range(n):
        ensemble.append(reglas[random.randint(0, len(reglas)-1)])
    return ensemble

def trainEnsemble(instances, ensemble):
    trainingValue = 0.0
    for instance in instances:
        trainingValue += schedule_builder_sum(instance, ensemble).bins_used
    return trainingValue

def simple_ensemble_combination(instances, reglas, size, nEnsembles):
    best = generarEnsembleAleatorio(size, reglas)
    costeBest = trainEnsemble(instances, best)
    print(costeBest) # podemos guardar la convergencia en un fichero, si queremos
    for i in range(1, nEnsembles):
        ensemble = generarEnsembleAleatorio(size, reglas)
        coste = trainEnsemble(instances, ensemble)
        if (coste < costeBest):
            costeBest = coste
            best = ensemble
            print(costeBest) # podemos guardar la convergencia en un fichero, si queremos
    return best


# RUN SEC
instancesNames = ['Falkenauer_t60_01.txt','Falkenauer_t60_11.txt','Falkenauer_t60_07.txt','Falkenauer_t60_18.txt']
instances = loadInstances(instancesNames) # se cargan las instancias

N = 100
reglas = generarPoblacionInicial(N) # podemos usar reglas random 
#reglas = load_rules("reglas.txt") # o cargar unas que tuviesemos previamente calculadas

# Training
#size = 3 # tamaño ensembles
#nEnsembles = 1000 # numero de ensembles que se generan
#print("Calculando ensembles...")
#inicio = time.time()
#ensemble = simple_ensemble_combination(instances, reglas, size, nEnsembles)
#fin = time.time()
#trainValue = trainEnsemble(instances, ensemble)
#print("Training:", trainValue)
#timeTraining = fin-inicio
#print("Tiempo entrenamiento:", timeTraining)
#print("Testing ensemble...")
#instancesNamesTest = ['Falkenauer_t120_07.txt', 'Falkenauer_t60_09.txt','Falkenauer_t249_01.txt','Falkenauer_u500_11.txt','Falkenauer_u120_01.txt']
#instancesTest = loadInstances(instancesNamesTest)
#testValue = trainEnsemble(instancesTest, ensemble)
#print("Test Ensemble: ", testValue)


schedule=3 # Elije entre el schedule_build er v1, v2 o v3
version= 2 # Elije entre el algoritmo PG v1 o v2 
if version == 2:
    print("Training GP...")
    inicio = time.time()
    solution, traza = genetic_programming_v2(instances, pop_size=50, num_generations=50, schedule=schedule)
    fin = time.time()
else:
    print("Training GP...")
    inicio = time.time()
    solution, traza = genetic_programming(instances, pop_size=50, num_generations=50, schedule=schedule)
    fin = time.time()

print("Representación montículo:", solution.getMonticulo())
print("Training:", solution.bins_used)
print("Tiempo entrenamiento:", fin-inicio)


# Guardar los datos de convergencia
r = random.randint(1, 10000000)
print("Guardando fichero convergencia", r)

fileName = "convergence_BPP_" + str(r) + ".csv"
file = []
file.append("Bins_used")
for valor in traza:
    file.append(str(valor))

writeFile(fileName, file)
# Calcular tiempo y guardar resumen
timeTraining = time.time() - inicio
print("Guardando fichero resumen", r)
fileName = "resumen_BPP_" + str(r) + ".csv"
resumen = "Training;    TimeTraining;   Regla;  Monticulo;\n" + str(solution.bins_used) + ";" + str(timeTraining) + ";" +str(solution.getRegla())+";"+ solution.getMonticulo() + "\n"
with open(fileName, 'w') as archivo:
    archivo.write(resumen)


print("Testing...")
instancesNamesTest = ['Falkenauer_t120_07.txt', 'Falkenauer_t60_09.txt','Falkenauer_t249_01.txt','Falkenauer_u500_11.txt','Falkenauer_u120_01.txt']
instancesTest = loadInstances(instancesNamesTest)
inicio = time.time()
test = train(instancesTest, solution,schedule)
fin = time.time()
print("Test:", test)
print("Tiempo test:", fin-inicio)
