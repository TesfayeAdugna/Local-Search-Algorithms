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