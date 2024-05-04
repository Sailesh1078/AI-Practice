# E SAILESWARA REDDY
# CS21B1078

import random
import math
from matplotlib import pyplot as plt
from copy import deepcopy

class City:
    def __init__(self, x=None, y=None):
        self.x = x if x is not None else random.randint(0, 10)
        self.y = y if y is not None else random.randint(0, 10)

    def dist(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Route(list):
    def __init__(self, cities=None):
        super(Route, self).__init__(cities or [])

    def cost(self):
        total = 0
        for i in range(len(self)-1):
            total += self[i].dist(self[i+1])
        total += self[-1].dist(self[0])
        return total

    def next_route(self):
        route = deepcopy(self)
        c1, c2 = random.sample(range(len(self)), 2)
        route[c1], route[c2] = route[c2], route[c1]
        return route

    def plot(self, title=None):
        X = [c.x for c in self] + [self[0].x]
        y = [c.y for c in self] + [self[0].y]
        plt.plot(X, y, 'o-')
        plt.title(title)
        plt.show()

def sim_ann(route, T, T0, alpha, schedule_type, max_iterations):
    all_iter = [(route, route.cost())]

    iteration = 0
    while T > T0 and iteration < max_iterations:
        next_route = route.next_route()
        next_cost = next_route.cost()
        dE = next_cost - route.cost()
        if dE < 0:
            route = next_route
        elif random.random() < math.exp(-dE/T):
            route = next_route
        else:
            continue
        all_iter.append((next_route, next_cost))
        if schedule_type == "gp":
            T *= alpha  # Update temperature using GP series
        elif schedule_type == "ap":
            T -= alpha  # Update temperature using AP series
        iteration += 1

    return all_iter

def plot_final_path(route, cost):
    route.plot(f"Final Path: Cost={cost:.2f}")

def progress_plot(all_iter):
    all_costs = [i[1] for i in all_iter]
    plt.plot(all_costs)
    plt.title(f"Progress over {len(all_iter)} iterations")
    plt.xlabel("Iterations")
    plt.ylabel("Cost")
    plt.show()

def main():
    print("Simulated Annealing Algorithm for TSP Optimization:\n")

    # Setting up initial parameters
    num_cities = 15
    min_temperature = 0.1
    cooling_factors = [0.97, 0.99]  # Experiment with different cooling factors
    starting_temperatures = [1e+10, 1e+12]  # Experiment with different starting temperatures
    max_iterations = 5000  # Maximum number of iterations

    # Generate random cities and initial route
    initial_route = Route([City() for _ in range(num_cities)])
    initial_cost = initial_route.cost()
    print("Initial State:", initial_route, f"Cost: {initial_cost:.2f}")
    initial_route.plot("Initial Route")

    for start_temp in starting_temperatures:
        for alpha in cooling_factors:
            print(f"\nRunning SA with starting temperature={start_temp} and cooling factor={alpha}...")
            # Running SA with GP series
            result_gp = sim_ann(initial_route, start_temp, min_temperature, alpha, "gp", max_iterations)
            final_route_gp, final_cost_gp = result_gp[-1]
            print(f"Final State (GP): {final_route_gp}, Cost: {final_cost_gp:.2f}")
            plot_final_path(final_route_gp, final_cost_gp)
            progress_plot(result_gp)

            # Running SA with AP series
            result_ap = sim_ann(initial_route, start_temp, min_temperature, alpha, "ap", max_iterations)
            final_route_ap, final_cost_ap = result_ap[-1]
            print(f"Final State (AP): {final_route_ap}, Cost: {final_cost_ap:.2f}")
            plot_final_path(final_route_ap, final_cost_ap)
            progress_plot(result_ap)

if __name__ == '__main__':
    main()