# E SAILESWARA REDDY
# CS21B1078

from collections import deque

# 8 Puzzle problem solver class
class Puzzle:
    def __init__(self, initial):
        self.initial_state = initial
        # Assuming The Goal State
        self.goal_state = [[1,0,3], [8,2,4], [7,6,5]]
        # Right, Up, Left, Down   
        self.rows = [1, 0, -1, 0]
        self.cols = [0, -1, 0, 1]
    
    def isSafe(self, x, y):  
        return x >= 0 and x < 3 and y >= 0 and y < 3  

    # Helper function to get successor states
    def get_successors(self, state):
        successors = []
        zero_pos = None
        # Find the position of the Empty tile
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    zero_pos = (i, j)
                    break
            if zero_pos:
                break
        
        # Generate successor states by moving the zero tile
        for i in range(4):
            new_x = zero_pos[0] + self.rows[i]
            new_y = zero_pos[1] + self.cols[i]
            if self.isSafe(new_x, new_y):
                new_state = [row[:] for row in state]
                new_state[zero_pos[0]][zero_pos[1]] = new_state[new_x][new_y]
                new_state[new_x][new_y] = 0
                successors.append(new_state)
        
        return successors

# BFS implementation
def bfs(puzzle):
    queue = deque()
    queue.append(([puzzle.initial_state], 0))  # (path, steps)

    while queue:
        path, steps = queue.popleft()
        current_state = path[-1]

        if current_state == puzzle.goal_state:
            return path, steps

        for successor in puzzle.get_successors(current_state):
            if successor not in path:
                new_path = path + [successor]
                queue.append((new_path, steps + 1))

# DFS implementation
def dfs(puzzle):
    stack = [([puzzle.initial_state], 0)]  # (path, steps)

    while stack:
        path, steps = stack.pop()
        current_state = path[-1]

        if current_state == puzzle.goal_state:
            return path, steps

        for successor in puzzle.get_successors(current_state):
            if successor not in path:
                new_path = path + [successor]
                stack.append((new_path, steps + 1))


# Main function
if __name__ == "__main__":
    # Assuming The Initial State
    initial = [[1,2,3], [8,6,4], [7,0,5]]
    puzzle = Puzzle(initial)

    # BFS
    print("BFS Solution:")
    bfs_path, bfs_steps = bfs(puzzle)
    for i, state in enumerate(bfs_path):
        print("Step", i, ":")
        for row in state:
            print(row)
        print()
    print("Number of steps required:", bfs_steps)
    print()

    # DFS
    print("DFS Solution:")
    dfs_path, dfs_steps = dfs(puzzle)
    for i, state in enumerate(dfs_path):
        print("Step", i, ":")
        for row in state:
            print(row)
        print()
    print("Number of steps required:", dfs_steps)
    print()
    
    print("Successfully Implemented BFS, DFS Algorithms, To Solve The 8 Puzzle Problem...")
    print()