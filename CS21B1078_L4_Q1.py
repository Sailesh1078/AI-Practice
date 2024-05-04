# E SAILESWARA REDDY
# CS21B1078

import heapq

# Function to find the minimum spanning tree using Prim's algorithm
def find_minimum_spanning_tree(graph):
    # Number of nodes in the graph
    num_nodes = len(graph)
    
    # Initialize visited nodes
    visited = [False] * num_nodes
    
    # Initialize arrays to store minimum spanning tree and its cost
    min_span_tree = [None] * num_nodes
    min_span_tree_cost = [float('inf')] * num_nodes
    min_span_tree_cost[0] = 0

    # Initialize priority queue
    priority_queue = [(0, 0)]  # (cost, node)

    # Loop until priority queue is empty
    while priority_queue:
        # Pop the node with minimum cost
        cost, node = heapq.heappop(priority_queue)
        visited[node] = True

        # Traverse neighbors of the current node
        for neighbor, weight in enumerate(graph[node]):
            if not visited[neighbor] and weight < min_span_tree_cost[neighbor]:
                # Update minimum spanning tree and its cost if a better path is found
                min_span_tree_cost[neighbor] = weight
                min_span_tree[neighbor] = node
                heapq.heappush(priority_queue, (weight, neighbor))

    return min_span_tree, min_span_tree_cost

# Function to solve the Traveling Salesman Problem using A* algorithm
def tsp_a_Star(adj_matrix):
    num_cities = len(adj_matrix)
    
    # Find minimum spanning tree of the graph
    min_span_tree, min_span_tree_cost = find_minimum_spanning_tree(adj_matrix)
    
    # Initialize sets of visited and unvisited cities
    unvisited_cities = set(range(num_cities))
    visited_cities = []
    start_city = 0

    # Heuristic function for A* algorithm
    h = lambda city: min(min_span_tree_cost[i] for i in unvisited_cities) + sum(min_span_tree_cost[i] for i in unvisited_cities) + min_span_tree_cost[city]


    # Initialize priority queue with starting city
    priority_queue = [(h(start_city), 0, [start_city], set([start_city]))]  # (f(n), g(n), path, visited)

    # Loop until priority queue is empty
    while priority_queue:
        _, cost, path, visited = heapq.heappop(priority_queue)
        # print(path)
        if len(visited) == num_cities:
            # Return to start city to complete the cycle
            cost += adj_matrix[path[-1]][start_city]
            path.append(start_city)
            return cost, path

        current_city = path[-1]

        # Traverse neighbors of the current city
        for neighbor, weight in enumerate(adj_matrix[current_city]):
            if neighbor not in visited:
                new_cost = cost + weight
                new_path = path + [neighbor]
                new_visited = visited.copy()
                new_visited.add(neighbor)
                # print(neighbor)
                heapq.heappush(priority_queue, (new_cost + h(neighbor), new_cost, new_path, new_visited))

    return float('inf'), None

# Given Graph
adjacency_matrix = [
    [0, 12, 10, 19, 8],
    [12, 0, 3, 7, 6],
    [10, 3, 0, 2, 20],
    [19, 7, 2, 0, 4],
    [8, 6, 20, 4, 0]
]

shortest_distance, shortest_path = tsp_a_Star(adjacency_matrix)

print("Shortest Distance:", shortest_distance)
print("Shortest Path:", shortest_path)
