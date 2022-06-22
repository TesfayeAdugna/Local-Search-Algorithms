from math import atan2, cos, sin, sqrt

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