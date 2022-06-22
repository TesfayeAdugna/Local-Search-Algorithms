import matplotlib.pyplot as plt
import math
import random

def readData():
    cities = []
    f = open("TSPgraph_files/texts3x.txt")
    for i in f.readlines():
        city_val = i.split()
        cities.append( [city_val[0], float(city_val[1]), float(city_val[2])])

    return cities


def calcDistance(cities):
    total_sum = 0
    for i in range(len(cities) - 1):
        cityA, cityB = cities[i], cities[i + 1]
        d = math.sqrt(math.pow(cityB[1] - cityA[1], 2) + math.pow(cityB[2] - cityA[2], 2))
        total_sum += d

    cityA, cityB = cities[0], cities[-1]
    d = math.sqrt(math.pow(cityB[1] - cityA[1], 2) + math.pow(cityB[2] - cityA[2], 2))
    total_sum += d

    return total_sum


def selectPopulation(cities, size):
    population = []

    for i in range(size):
        c = cities.copy()
        random.shuffle(c)
        distance = calcDistance(c)
        population.append([distance, c])
    fitest = sorted(population)[0]

    return population, fitest


def geneticAlgorithm(population, lenCities, TOURNAMENT_SELECTION_SIZE, MUTATION_RATE, CROSSOVER_RATE, TARGET,):
    gen_number = 0
    for i in range(200):
        new_population = []
        new_population.append(sorted(population)[0])
        new_population.append(sorted(population)[1])

        for i in range(int((len(population) - 2) / 2)):
            random_number = random.random()
            if random_number < CROSSOVER_RATE:
                parent_chromosome1 = sorted( random.choices(population, k=TOURNAMENT_SELECTION_SIZE))[0]
                parent_chromosome2 = sorted( random.choices(population, k=TOURNAMENT_SELECTION_SIZE))[0]

                point = random.randint(0, lenCities - 1)

                child_chromosome1 = parent_chromosome1[1][0:point]
                for j in parent_chromosome2[1]:
                    if (j in child_chromosome1) == False:
                        child_chromosome1.append(j)

                child_chromosome2 = parent_chromosome2[1][0:point]
                for j in parent_chromosome1[1]:
                    if (j in child_chromosome2) == False:
                        child_chromosome2.append(j)

            else:
                child_chromosome1, child_chromosome2 = random.choices(population)[0][1], random.choices(population)[0][1]

            if random.random() < MUTATION_RATE:
                point1 = random.randint(0, lenCities - 1)
                point2 = random.randint(0, lenCities - 1)
                child_chromosome1[point1], child_chromosome1[point2] = (
                    child_chromosome1[point2],
                    child_chromosome1[point1],
                )

                point1 = random.randint(0, lenCities - 1)
                point2 = random.randint(0, lenCities - 1)
                child_chromosome2[point1], child_chromosome2[point2] = (
                    child_chromosome2[point2],
                    child_chromosome2[point1],
                )

            new_population.append([calcDistance(child_chromosome1), child_chromosome1])
            new_population.append([calcDistance(child_chromosome2), child_chromosome2])

        population = new_population

        gen_number += 1

        if gen_number % 10 == 0:
            print(gen_number, sorted(population)[0][0])

        if sorted(population)[0][0] < TARGET:
            break

    answer = sorted(population)[0]

    return answer, gen_number


# draw cities and answer map
# def drawMap(city, answer):
#     for j in city:
#         plt.plot(j[1], j[2], "ro")
#         plt.annotate(j[0], (j[1], j[2]))

#     for i in range(len(answer[1])):
#         try:
#             first = answer[1][i]
#             secend = answer[1][i + 1]

#             plt.plot([first[1], secend[1]], [first[2], secend[2]], "gray")
#         except:
#             continue

#     first = answer[1][0]
#     secend = answer[1][-1]
#     plt.plot([first[1], secend[1]], [first[2], secend[2]], "gray")

#     plt.show()


def main():
    POPULATION_SIZE = 2000
    TOURNAMENT_SELECTION_SIZE = 4
    MUTATION_RATE = 0.1
    CROSSOVER_RATE = 0.9
    TARGET = 450.0

    cities = readData()
    firstPopulation, firstFitest = selectPopulation(cities, POPULATION_SIZE)
    answer, genNumber = geneticAlgorithm(
        firstPopulation,
        len(cities),
        TOURNAMENT_SELECTION_SIZE,
        MUTATION_RATE,
        CROSSOVER_RATE,
        TARGET,
    )

    print("Generation: " + str(genNumber), "\nbefore training: " + str(firstFitest[0]), "\nafter training: " + str(answer[0]), "\nTarget distance: " + str(TARGET))


main()