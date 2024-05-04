# E SAILESWARA REDDY
# CS21B1078

from collections import deque

# Tower of Hanoi problem solver class
class TowerOfHanoi:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.initial_state = [list(range(num_disks, 0, -1)), [], []]
        self.goal_state = [[], [], list(range(num_disks, 0, -1))]

    # Helper function to get successor states
    def get_successors(self, state):
        successors = []
        for i, tower in enumerate(state):
            if tower:
                for j, other_tower in enumerate(state):
                    if i != j and (not other_tower or other_tower[-1] > tower[-1]):
                        new_state = [tower.copy() for tower in state]
                        disk = new_state[i].pop()
                        new_state[j].append(disk)
                        successors.append(new_state)
        return successors

# BFS implementation
def bfs(tower_of_hanoi):
    queue = deque()
    queue.append([tower_of_hanoi.initial_state])

    while queue:
        path = queue.popleft()
        current_state = path[-1]

        if current_state == tower_of_hanoi.goal_state:
            return path

        for successor in tower_of_hanoi.get_successors(current_state):
            if successor not in path:
                new_path = path + [successor]
                queue.append(new_path)

# DFS implementation
def dfs(tower_of_hanoi):
    stack = [[tower_of_hanoi.initial_state]]

    while stack:
        path = stack.pop()
        current_state = path[-1]

        if current_state == tower_of_hanoi.goal_state:
            return path

        for successor in tower_of_hanoi.get_successors(current_state):
            if successor not in path:
                new_path = path + [successor]
                stack.append(new_path)

# IDS implementation
def ids(tower_of_hanoi):
    depth_limit = 0

    while True:
        result = dls(tower_of_hanoi, depth_limit)
        if result:
            return result
        depth_limit += 1

# Depth-limited search (DLS) used by IDS
def dls(tower_of_hanoi, depth_limit):
    stack = [[tower_of_hanoi.initial_state]]

    while stack:
        path = stack.pop()
        current_state = path[-1]

        if current_state == tower_of_hanoi.goal_state:
            return path

        if len(path) <= depth_limit:
            for successor in tower_of_hanoi.get_successors(current_state):
                if successor not in path:
                    new_path = path + [successor]
                    stack.append(new_path)


# Main function
if __name__ == "__main__":
    # Given parameters
    num_disks = 3
    tower_of_hanoi = TowerOfHanoi(num_disks)

    # BFS
    print("BFS Solution:")
    bfs_path = bfs(tower_of_hanoi)
    for state in bfs_path:
        print(state)
    print()

    # DFS
    print("DFS Solution:")
    dfs_path = dfs(tower_of_hanoi)
    for state in dfs_path:
        print(state)
    print()

    # IDS
    print("IDS Solution:")
    ids_path = ids(tower_of_hanoi)
    for state in ids_path:
        print(state)
    print()

    print("Successfully Implemented BFS, DFS, IDS Algorithms, To Solve The Tower Of Hanoi Problem...")