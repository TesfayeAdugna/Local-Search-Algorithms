import numpy as np
from LoadKnapsack import LoadGraph_knapsack
from LoadTSP import LoadGraph_TSP

# knapsack problem using simulated annealing algorithm starts here.
class KnapSack:

    def __init__(self) -> None:
        pass

    def check_weight(self, packing, Items, max_weight):
        val, weight = 0.0, 0.0
        for i in range(len(packing)):
            if packing[i] == 1:
                val += Items[i][0]
                weight += Items[i][1]
        if weight > max_weight:
            val = 0.0
        return (val, weight)

    def findNeighbour(self, packing, rand):
        res, i = packing.copy(), rand.randint(len(packing))
        if res[i] == 0:
            res[i] = 1
        elif res[i] == 1:
            res[i] = 0
        return res

    def simulatedAnnealing(self, Items, max_weight):
        for i in range(len(Items)):
            Items[i] = Items[i][::-1]

        T = 10000.0
        rand = np.random.RandomState(5)
        current_solution = np.ones(len(Items), dtype=np.int64)
        (current_val, current_weight) = self.check_weight(current_solution, Items, max_weight)
        n = 1000
        for i in range(n):
            neighbour_pack = self.findNeighbour(current_solution, rand)
            (neighbour_val, neighbour_weight) = self.check_weight(neighbour_pack, Items, max_weight)
            if neighbour_val > current_val:
                current_solution, current_val = neighbour_pack, neighbour_val
            else:
                acceptance_prob = np.exp((neighbour_val - current_val ) / T ) 
                prob = rand.random()
                if prob < acceptance_prob:
                    current_solution, current_val = neighbour_pack, neighbour_val
            if T < 0.00000000001:
                T = 0.00000000001
            else:
                T *= (1 - i/n)

        (v,s) = self.check_weight(current_solution, Items, max_weight)

        return current_solution, v, s
# Knapsack problem using simulated annealing algorithm ends here.


# Travelling salesman problem using simulated annealing algorithm starts here.
class TSP:

    def __init__(self) -> None:
        pass

    def check_weight(self, packing, Items, max_weight):
        val, weight = 0.0, 0.0
        for i in range(len(packing)):
            if packing[i] == 1:
                val += Items[i][0]
                weight += Items[i][1]
        if weight > max_weight:
            val = 0.0
        return (val, weight)

    def findNeighbour(self, packing, rand):
        res, i = packing.copy(), rand.randint(len(packing))
        if res[i] == 0:
            res[i] = 1
        elif res[i] == 1:
            res[i] = 0
        return res

    def simulatedAnnealing(self, Items, max_weight):
        for i in range(len(Items)):
            Items[i] = Items[i][::-1]

        T = 10000.0
        rand = np.random.RandomState(5)
        current_solution = np.ones(len(Items), dtype=np.int64)
        (current_val, current_weight) = self.check_weight(current_solution, Items, max_weight)
        n = 1000
        for i in range(n):
            neighbour_pack = self.findNeighbour(current_solution, rand)
            (neighbour_val, neighbour_weight) = self.check_weight(neighbour_pack, Items, max_weight)
            if neighbour_val > current_val:
                current_solution, current_val = neighbour_pack, neighbour_val
            else:
                acceptance_prob = np.exp((neighbour_val - current_val ) / T ) 
                prob = rand.random()
                if prob < acceptance_prob:
                    current_solution, current_val = neighbour_pack, neighbour_val
            if T < 0.00000000001:
                T = 0.00000000001
            else:
                T *= (1 - i/n)

        (v,s) = self.check_weight(current_solution, Items, max_weight)

        return current_solution, v, s


if __name__ == "__main__":
    # Test Knapsack using simulated annealing.
    l = LoadGraph_knapsack("Knapsackgraph_files/texts1x.txt")
    Items, max_w = l.items, l.max_weight
    k = KnapSack()
    pack, TotalVal, weight = k.simulatedAnnealing(Items, max_w)
    print("Items: ", end="")
    for i in range(len(pack)):
        if pack[i] == 1:
            print(l.ItemCollection[i], end=" ")
    print("\nTotal Value: ", TotalVal)

    # Test TSP using simulated annealing.