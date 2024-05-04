# E SAILESWARA REDDY
# CS21B1078

from collections import deque

# The Two Jug problem solver class
class WaterJugProblem:
    def __init__(self, jug1_capacity, jug2_capacity, target_amount):
        self.jug1_capacity = jug1_capacity
        self.jug2_capacity = jug2_capacity
        self.target_amount = target_amount
        self.initial_state = (0, 0)  # Initial state: both jugs are empty
        self.goal_state = (target_amount, 0)  # Goal state: 1 liter of water in jug J1

    def get_successors(self, state):
        successors = []

        # Fill jug1
        if state[0] < self.jug1_capacity:
            successors.append((self.jug1_capacity, state[1]))

        # Fill jug2
        if state[1] < self.jug2_capacity:
            successors.append((state[0], self.jug2_capacity))

        # Empty jug1
        if state[0] > 0:
            successors.append((0, state[1]))

        # Empty jug2
        if state[1] > 0:
            successors.append((state[0], 0))

        # Pour from jug1 to jug2
        pour_amount = min(state[0], self.jug2_capacity - state[1])
        if pour_amount > 0:
            successors.append((state[0] - pour_amount, state[1] + pour_amount))

        # Pour from jug2 to jug1
        pour_amount = min(state[1], self.jug1_capacity - state[0])
        if pour_amount > 0:
            successors.append((state[0] + pour_amount, state[1] - pour_amount))

        return successors

# BFS implementation
def bfs(water_jug_problem):
    queue = deque()
    queue.append([water_jug_problem.initial_state])

    while queue:
        path = queue.popleft()
        current_state = path[-1]

        if current_state == water_jug_problem.goal_state:
            return path

        for successor in water_jug_problem.get_successors(current_state):
            if successor not in path:
                new_path = path + [successor]
                queue.append(new_path)

# DFS implementation
def dfs(water_jug_problem):
    stack = [[water_jug_problem.initial_state]]

    while stack:
        path = stack.pop()
        current_state = path[-1]

        if current_state == water_jug_problem.goal_state:
            return path

        for successor in water_jug_problem.get_successors(current_state):
            if successor not in path:
                new_path = path + [successor]
                stack.append(new_path)

# IDS implementation
def ids(water_jug_problem):
    depth_limit = 0

    while True:
        result = dls(water_jug_problem, depth_limit)
        if result:
            return result
        depth_limit += 1

# Depth-limited search (DLS) used by IDS
def dls(water_jug_problem, depth_limit):
    stack = [[water_jug_problem.initial_state]]

    while stack:
        path = stack.pop()
        current_state = path[-1]

        if current_state == water_jug_problem.goal_state:
            return path

        if len(path) <= depth_limit:
            for successor in water_jug_problem.get_successors(current_state):
                if successor not in path:
                    new_path = path + [successor]
                    stack.append(new_path)

# Main function
if __name__ == "__main__":
    # Given parameters
    jug1_capacity = 3
    jug2_capacity = 5
    target_amount = 1

    water_jug_problem = WaterJugProblem(jug1_capacity, jug2_capacity, target_amount)

    # BFS
    print("BFS Solution:")
    bfs_path = bfs(water_jug_problem)
    for state in bfs_path:
        print(state)

    print()

    # DFS
    print("DFS Solution:")
    dfs_path = dfs(water_jug_problem)
    for state in dfs_path:
        print(state)

    print()

    # IDS
    print("IDS Solution:")
    ids_path = ids(water_jug_problem)
    for state in ids_path:
        print(state)
    print()
    
    print("Successfully Implemented BFS, DFS, IDS Algorithms, To Solve The Two Jug Problem...")
