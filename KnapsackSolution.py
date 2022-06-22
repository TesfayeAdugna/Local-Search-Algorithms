from math import sin, cos, sqrt, atan2
import numpy as np
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

    
    # KnapSack problem using simulated annealing

    # items  0  1  2  3  4  5  6  7  8  9
    # valus 79 32 47 18 26 85 33 40 45 59
    # sizes 85 26 48 21 22 95 43 45 55 52
    # max size = 101

    # maximize value

    def total_valu_size(self, packing, valus, sizes, max_size):
        # total value and size of a specified packing
        v = 0.0  # total valu of packing
        s = 0.0  # total size of packing
        n = len(packing)
        for i in range(n):
            if packing[i] == 1:
                v += valus[i]
                s += sizes[i]
        if s > max_size:  # too big to fit in knapsack
            v = 0.0
        return (v, s)

    def adjacent(self, packing, rnd):
        n = len(packing)
        result = np.copy(packing)
        i = rnd.randint(n)
        if result[i] == 0:
            result[i] = 1
        elif result[i] == 1:
            result[i] = 0
        return result

    def solve(self, n_items, rnd, valus, sizes, max_size, \
        max_iter, start_temperature, alpha):
        # solve using simulated annealing
        curr_temperature = start_temperature
        curr_packing = np.ones(n_items, dtype=np.int64)
        print("Initial guess: ")
        print(curr_packing)

        (curr_valu, curr_size) = self.total_valu_size(curr_packing, valus, sizes, max_size)
        iteration = 0
        interval = (int)(max_iter / 10)
        while iteration < max_iter:
            # pct_iters_left = \
            #  (max_iter - iteration) / (max_iter * 1.0)
            adj_packing = self.adjacent(curr_packing, rnd)
            (adj_v, _) = self.total_valu_size(adj_packing, \
            valus, sizes, max_size)

            if adj_v > curr_valu:  # better so accept adjacent
                curr_packing = adj_packing; curr_valu = adj_v
            else:          # adjacent packing is worse
                accept_p = np.exp( (adj_v - curr_valu ) / curr_temperature ) 
            p = rnd.random()
            if p < accept_p:  # accept worse packing anyway
                curr_packing = adj_packing; curr_valu = adj_v 
            # else don't accept

            if iteration % interval == 0:
                print("iter = %6d : curr value = %7.0f : curr temp = %10.2f " % (iteration, curr_valu, curr_temperature))

            if curr_temperature < 0.00001:
                curr_temperature = 0.00001
            else:
                curr_temperature *= alpha
            # curr_temperature = start_temperature * \
            # pct_iters_left * 0.0050
            iteration += 1

        return curr_packing       

    def main(self):
        
        valus = np.array([79, 32, 47, 18, 26, 85, 33, 40, 45, 59])
        sizes = np.array([85, 26, 48, 21, 22, 95, 43, 45, 55, 52])
        max_size = 101

        print("\nItem values: ")
        print(valus)
        print("\nItem sizes: ")
        print(sizes)
        print("\nMax total size = %d " % max_size)

        rnd = np.random.RandomState(5)  # 3 .98 = 117,100
        max_iter = 1000
        start_temperature = 10000.0
        alpha = 0.98

        print("\nSettings: ")
        print("max_iter = %d " % max_iter)
        print("start_temperature = %0.1f " \
            % start_temperature)
        print("alpha = %0.2f " % alpha)

        print("\nStarting solve() ")
        packing = self.solve(10, rnd, valus, sizes, max_size, max_iter, start_temperature, alpha)
        print("Finished solve() ")

        print("\nBest packing found: ")
        print(packing)
        (v,s) = self.total_valu_size(packing, valus, sizes, max_size)
        print("\nTotal value of packing = %0.1f " % v)
        print("Total size  of packing = %0.1f " % s)

        print("\nEnd demo ")
            





    def knapsack_Genetic(self):
        pass


if __name__ == "__main__":
    l = LoadGraph_knapsack("Knapsackgraph_files/texts1x.txt")
    k = Knapsack()
    print(l.items)
    Items, TotalValue = k.hillClimbing(l.items, l.max_weight)
    answer = []
    for i in Items:
        answer.append(l.ItemCollection[i])
    print("items: ", answer, "\nTotal value: ", TotalValue)