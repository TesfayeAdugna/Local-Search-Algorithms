from math import atan2, cos, sin, sqrt
import random

# for this problem we will be using the huiristic data to simplify the searching
# algorithm. we will assume the man uses plane to visit the cities. that way we
# can check the possiplities and find the shortest path for the man.
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


    def TSP_simulated_annealing(self):
        pass

    def TSP_Genetic(self):
        pass


if __name__ == "__main__":
    # testing the Traveling sales person using Hill climbing.
    # you can use the three graph_files to test this algorithm.
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