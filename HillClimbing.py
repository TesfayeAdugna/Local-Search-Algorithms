from math import atan2, cos, sin, sqrt
import random

# Knapsack problem using hill climbing algorithm code starts here.
class LoadGraph_knapsack:
    
    def __init__(self, filename):
        self.ItemCollection = {}
        self.max_weight = 0
        self.items = []
        i = 0
        with open(filename) as file:
            for line in file:
                i+=1
                if i == 2:
                    continue
                con = line.split(",")
                if i>2:
                    self.ItemCollection[i-3] = con[0]
                if len(con) < 3:
                    self.max_weight = int(con[0])
                    continue
                temp =[]
                temp.append(float(con[1]))
                temp.append(int(con[2]))
                self.items.append(temp)


class Knapsack:
    
    def __init__(self):
        pass

    # helping functions
    def calcRouteLength(self, knapsack, solution):
        routeLength = 0
        for i in range(len(solution)):
            routeLength += knapsack[solution[i]][1]
        return routeLength # returns total value.

    def findNeighbours(self, solution):
        neighbours = []
        for i in range(len(solution)):
            for j in range(i + 1, len(solution)):
                neighbour = solution.copy()
                neighbour[i] = solution[j]
                neighbour[j] = solution[i]
                neighbours.append(neighbour)
        return neighbours

    def findBestNeighbour(self, knapsack, neighbours):
        if neighbours:
            bestRouteLength = self.calcRouteLength(knapsack, neighbours[0])
            bestNeighbour = neighbours[0]
            for neighbour in neighbours:
                currentRouteLength = self.calcRouteLength(knapsack, neighbour)
                if currentRouteLength > bestRouteLength:
                    bestRouteLength = currentRouteLength
                    bestNeighbour = neighbour
            return bestNeighbour, bestRouteLength
        else:
            return neighbours, 0

    def hillClimbing(self, knapsack, maxweight):
        # choosing initial state
        cities = list(range(len(knapsack)))
        currentSolution = []
        temp = 0
        for _ in range(len(cities)):
            ran = random.randint(0, len(cities)-1)
            randomCity = cities[ran]
            temp += knapsack[randomCity][0]
            if temp <= maxweight:
                currentSolution.append(randomCity)
                cities.remove(randomCity)
            else:
                temp -= knapsack[randomCity][0]

        currentRouteLength = self.calcRouteLength(knapsack, currentSolution)
        neighbours = self.findNeighbours(currentSolution)
        bestNeighbour, bestNeighbourRouteLength = self.findBestNeighbour(knapsack, neighbours)

        while bestNeighbourRouteLength > currentRouteLength:
            currentSolution = bestNeighbour
            currentRouteLength = bestNeighbourRouteLength
            neighbours = self.findNeighbours(currentSolution)
            bestNeighbour, bestNeighbourRouteLength = self.findBestNeighbour(knapsack, neighbours)

        return currentSolution, currentRouteLength

# Knapsack problem using hill climbing algorithm ends here.


# Travelling salesman problem algorithm starts here.
class LoadGraph_TSP:

    def __init__(self, filename):
        self.CityCollection = {}
        self.cities = {}
        with open(filename) as file:
            i = 0
            for line in file:
                con = line.split()
                self.CityCollection[i] = con[0]
                self.cities[con[0]] = (float(con[1]), float(con[2]))
                i += 1

    def create_problem(self):
        problem = []
        for i in self.cities:
            temp = []
            for j in self.cities:
                Haversine = sin((self.cities[j][0]-self.cities[i][0]) / 2)**2 + cos(self.cities[j][0]) * cos(self.cities[i][0]) * sin((self.cities[j][1]-self.cities[i][1]) / 2)**2
                c = 2 * atan2(sqrt(Haversine), sqrt(1 - Haversine))
                temp.append(6373.0 * c)

            problem.append(temp)

        return problem


class TSP:

    def __init__(self):
        pass

    # helping functions
    def calcRouteLength(self, tsp, solution):
        routeLength = 0
        for i in range(len(solution)):
            routeLength += tsp[solution[i - 1]][solution[i]]
        return routeLength

    def findNeighbours(self, solution):
        neighbours = []
        for i in range(len(solution)):
            for j in range(i + 1, len(solution)):
                neighbour = solution.copy()
                neighbour[i] = solution[j]
                neighbour[j] = solution[i]
                neighbours.append(neighbour)
        return neighbours

    def findBestNeighbour(self, tsp, neighbours):
        bestRouteLength = self.calcRouteLength(tsp, neighbours[0])
        bestNeighbour = neighbours[0]
        for neighbour in neighbours:
            currentRouteLength = self.calcRouteLength(tsp, neighbour)
            if currentRouteLength < bestRouteLength:
                bestRouteLength = currentRouteLength
                bestNeighbour = neighbour
        return bestNeighbour, bestRouteLength

    def hillClimbing(self, tsp):
        cities = list(range(len(tsp)))
        currentSolution = []
        for _ in range(len(tsp)):
            ran = random.randint(0, len(cities)-1)
            randomCity = cities[ran]
            currentSolution.append(randomCity)
            cities.remove(randomCity)

        currentRouteLength = self.calcRouteLength(tsp, currentSolution)
        neighbours = self.findNeighbours(currentSolution)
        bestNeighbour, bestNeighbourRouteLength = self.findBestNeighbour(tsp, neighbours)

        while bestNeighbourRouteLength < currentRouteLength:
            currentSolution = bestNeighbour
            currentRouteLength = bestNeighbourRouteLength
            neighbours = self.findNeighbours(currentSolution)
            bestNeighbour, bestNeighbourRouteLength = self.findBestNeighbour(tsp, neighbours)

        return currentSolution, currentRouteLength

# Travelling sales man problem ends here.


if __name__ == "__main__":
    # knapsack problem test.
    # l = LoadGraph_knapsack("Knapsackgraph_files/texts1x.txt")
    # k = Knapsack()
    # Items, TotalValue = k.hillClimbing(l.items, l.max_weight)
    # answer = []
    # for i in Items:
    #     answer.append(l.ItemCollection[i])
    # print("items: ", answer, "\nTotal value: ", TotalValue)

    # Travelling sales man problem test
    t = TSP()
    l = LoadGraph_TSP("TSPgraph_files/texts2x.txt")
    tsp = l.create_problem()
    Cities, totallength = t.hillClimbing(tsp)
    answer = []
    for i in Cities:
        answer.append(l.CityCollection[i])

    print("path: ", end="")
    [print(x, "-->", end="") for x in answer]
    print("\nTotal Length: ", totallength)