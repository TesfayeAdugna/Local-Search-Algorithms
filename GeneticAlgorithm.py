from typing import List
import random
from LoadKnapsack import LoadGraph_knapsack


class Individual:
    def __init__(self, genes):
        self.genes = genes
    
    def fitness(self):
        tot_weight=0
        for i,g in zip(items,self.genes):
            tot_weight+=i.weight*g
        
        tot_val=0
        for i,g in zip(items,self.genes):
            tot_val+=i.value*g
        
        
        if tot_weight <= max_weight:
            return tot_val
        
        return 0
    def __str__(self):
        return repr(self.genes)

    def __hash__(self):
        return hash(str(self.genes))
class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


max_weight = 15
cross_rate = 0.53
mut_rate = 0.013
rep_rate = 0.15

it = LoadGraph_knapsack("Knapsackgraph_files/texts1x.txt")
ite = it.items
lst = []
for key in it.ItemCollection:
    temp = [it.ItemCollection[key]]
    lst.append(temp)
for i in range(len(ite)):
    lst[i].extend(ite[i])

items = []
for i in range(len(lst)):
    j = Item(lst[i][0],lst[i][1],lst[i][2])
    items.append(j)

name_items = [i.name for i in items]


def Initial_population():
    c=6
    population = []
    while len(population) != c:
        
        genes=[]
        ch=[0,1]
        for i in items:
            genes.append(random.choice(ch))
        
        population.append(Individual(genes))

    return population


def selected(population):
    parents = []
    
    
    random.shuffle(population)

    # we use the first 4 individuals
    # run a tournament between them and
    # get two fit parents for the next steps of evolution

    # tournament between first and second
    if population[0].fitness() > population[1].fitness():
        parents.append(population[0])
    else:
        parents.append(population[1])
    
    # tournament between third and fourth
    if population[2].fitness() > population[3].fitness():
        parents.append(population[2])
    else:
        parents.append(population[3])

    return parents


def mate(parents):
    n = len(items)

    first_child = parents[1].genes[n//2:] + parents[0].genes[:n//2]
    second_child = parents[1].genes[:n//2] + parents[0].genes[n//2:]

    return [Individual(first_child), Individual(second_child)]


def mutate(individuals):
    for ind in individuals:
        for i in range(len(ind.genes)):
            if random.random() < mut_rate:
                # Flip the gene
                ind.genes[i] = ~ind.genes[i]


def new_generation(population):
    new_gen = []
    while len(new_gen) < len(population):
        children = []

        # we run selected and get parents
        parents = selected(population)

        # reproduction
        if random.random() < rep_rate:
            children = parents
        else:
            # mate
            if random.random() < cross_rate:
                children = mate(parents)
            
            # mutation
            if random.random() < mut_rate:
                mutate(children)

        new_gen.extend(children)

    return new_gen[:len(population)]


def average_fitness(population):
    return sum([i.fitness() for i in population]) / len(population)


def main():
    population = Initial_population()

    averageFitness = []

    for i in range(500):
        averageFitness.append(average_fitness(population))
        population = new_generation(population)

    population = sorted(population, key=lambda i: i.fitness(), reverse=True)
    return population[0]

print([(name,val) for name,val in zip(name_items,main().genes)])