from math import sin, cos, sqrt, atan2
import random

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

    def knapsack_simulated_annealing(self):
        pass

    def knapsack_Genetic(self):
        pass


if __name__ == "__main__":
    l = LoadGraph_knapsack("Knapsackgraph_files/texts1x.txt")
    k = Knapsack()
    Items, TotalValue = k.hillClimbing(l.items, l.max_weight)
    answer = []
    for i in Items:
        answer.append(l.ItemCollection[i])
    print("items: ", answer, "\nTotal value: ", TotalValue)