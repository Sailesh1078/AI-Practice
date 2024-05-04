import numpy as np

class KnapsackSolver:
    def __init__(self, weights, values, capacity):
        self.weights = weights
        self.values = values
        self.capacity = capacity
        self.numItems = len(weights)
        
    def solve(self):
        openList = [((), 0, 0)]  # (items included, total weight, total value)

        for i in range(self.numItems):
            knapsack, totalWeight, totalValue = openList.pop(0)
            fN1, fN2 = -1, -1

            # Include 'i'th element
            if totalWeight + self.weights[i] <= self.capacity:
                knapsackIncl = (knapsack + (i,), totalWeight + self.weights[i], totalValue + self.values[i])
                hN1 = self.heuristic(self.weights[i + 1:], self.values[i + 1:], self.capacity - knapsackIncl[1])
                fN1 = totalValue + self.values[i] + hN1

            # Not include 'i'th element
            knapsackNotIncl = (knapsack, totalWeight, totalValue)
            hN2 = self.heuristic(self.weights[i + 1:], self.values[i + 1:], self.capacity - knapsackNotIncl[1])
            fN2 = totalValue + hN2

            if fN1 == -1:
                openList.append(knapsackNotIncl)
            else:
                if fN1 <= fN2:
                    openList.append(knapsackNotIncl)
                else:
                    openList.append(knapsackIncl)

        return openList.pop(0)

    def heuristic(self, weights, values, capacity):
        if len(weights) == 0:
            return 0

        # Calculate the value-to-weight ratio
        valueWeightRatio = np.array(values) / np.array(weights)
        # Sort items by the value-to-weight ratio in descending order
        greedyOrder = np.argsort(valueWeightRatio)[::-1]

        totalWeight = 0
        totalValue = 0

        # Greedily select items based on value-to-weight ratio until capacity is reached
        for i in greedyOrder:
            if weights[i] + totalWeight <= capacity:
                totalWeight += weights[i]
                totalValue += values[i]
            else:
                break

        return totalValue


def main():
    # Given Parameters 
    weights = [100, 1000, 3000, 10, 2000]
    values = [1000, 2000,4000, 5000, 5000]
    capacity = 4000

    solver = KnapsackSolver(weights, values, capacity)
    maxKnapsack, totalWeight, totalValue = solver.solve()

    print("Items in the knapsack:", *maxKnapsack)
    print("Total weight of knapsack:", totalWeight)
    print("Total value of knapsack:", totalValue)

if __name__ == "__main__":
    main()
