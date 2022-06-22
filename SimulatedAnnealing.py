import numpy as np
from KnapsackSolution import LoadGraph_knapsack

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

        curr_temperature = 10000.0
        rand = np.random.RandomState(5)
        alpha = 0.98
        curr_packing = np.ones(len(Items), dtype=np.int64)
        (curr_valu, curr_size) = self.check_weight(curr_packing, Items, max_weight)
        iteration = 0
        max_iter = 1000
        while iteration < max_iter:
            adj_packing = self.findNeighbour(curr_packing, rand)
            (adj_v, _) = self.check_weight(adj_packing, Items, max_weight)
            if adj_v > curr_valu:
                curr_packing = adj_packing
                curr_valu = adj_v
            else:
                accept_p = np.exp( (adj_v - curr_valu ) / curr_temperature ) 
                p = rand.random()
                if p < accept_p:
                    curr_packing = adj_packing
                    curr_valu = adj_v 
            if curr_temperature < 0.00001:
                curr_temperature = 0.00001
            else:
                curr_temperature *= alpha
            iteration += 1

        (v,s) = self.check_weight(curr_packing, Items, max_weight)

        return curr_packing, v, s


if __name__ == "__main__":
    l = LoadGraph_knapsack("Knapsackgraph_files/texts1x.txt")
    Items, max_w = l.items, l.max_weight
    k = KnapSack()
    pack, TotalVal, weight = k.simulatedAnnealing(Items, max_w)
    print("Items: ", end="")
    for i in range(len(pack)):
        if pack[i] == 1:
            print(l.ItemCollection[i], end=" ")
    print("\nTotal Value: ", TotalVal, "\nTotal weight: ", weight)