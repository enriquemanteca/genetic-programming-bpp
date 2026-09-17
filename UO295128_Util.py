import random
import numpy as np

## basic
class BinPackingInstance:
    def __init__(self, name, dimension, capacity ,objects):
        self.name = name
        self.dimension = int(dimension)
        self.capacity = int(capacity)
        self.objects = objects

class BinPackingSolution:
    def __init__(self, display):
        self.display = display
        self.bins_used = total_bins(display)
        #   El display es una lista de tamaño=num_objetos en el que cada posición dice en que contenedor va guardado el objeto de dicha posición
        # es decir, para si el objeto objects[3] va en el contenedor 2, diplay[3]=2.
        #   El valor de bins_used será el valor máximo de display

def distance(city1, city2):
    return ((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)**0.5

def total_bins(display):
    total_bins_used=max(display)
    return total_bins_used

## carga instancia
def load_binpacking_instance(filename):
    file = "instances/" + filename # OJO AQUI SI SE MUEVEN LAS INSTANCIAS A OTRA CARPETA!
    with open(file, 'r') as f:
        lines = f.readlines()
        objetos = []
        for i,line in enumerate(lines):
            if i==0:
                dimension = line
            elif i==1:
                bin_capacity= line
            else:
                if line.strip() == "":
                    break
                objetos.append(int(line))
        return dimension, bin_capacity, objetos

def create_binpacking_instance(name, dimension, capacity ,objects):
    return BinPackingInstance(name, dimension, capacity ,objects)

## validar soluciones
def validate_binpacking_solution(solution, instance):
    objects = instance.objects
    num_objects = instance.dimension
    bincapacity=instance.capacity
    display = solution.display
    val=np.zeros(num_objects)


    if len(display) != num_objects:
        print("No se han guardado todos los objetos")
        return False


    # Se suma en un array el valor almacenado en cada contenedor
    for i, object_bin in enumerate(display):
        val[object_bin] += objects[i]
        if object==0:
            return False

    i=0    
    while val[i]!=0 or i<num_objects:
        if val[i]>bincapacity:
            return False
        i +=1


    calculated_bins_used = total_bins(display)
    if calculated_bins_used != solution.bins_used:
        print("No coincide")
        return False
    return True

# cargar instancias para el GP
def loadInstances(instancesNames):
    instances = []
    for name in instancesNames:
        dimension, capacity, objects = load_binpacking_instance(name)
        binpacking_instance = create_binpacking_instance(name, dimension, capacity, objects)
        instances.append(binpacking_instance)
    return instances

# guardar los resultados en un fichero
def writeFile(file_path, l):
    with open(file_path, 'w') as file:
        for item in l:
            file.write(str(item) + '\n')