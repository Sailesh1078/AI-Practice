# E SAILESWARA REDDY
# CS21B1078

import numpy as np
from collections import defaultdict

class Agent:
    # Define class constants for directions and actions
    LEFT = {'NORTH': 'WEST', 'WEST': 'SOUTH', 'SOUTH': 'EAST', 'EAST': 'NORTH'}
    RIGHT = {'NORTH': 'EAST', 'EAST': 'SOUTH', 'SOUTH': 'WEST', 'WEST': 'NORTH'}
    FORWARD = {'NORTH': (0, 1), 'EAST': (1, 0), 'SOUTH': (0, -1), 'WEST': (-1, 0)}
    TURNS = {
        ('NORTH', 'NORTH'): [], ('NORTH', 'EAST'): ['RIGHT'], ('NORTH', 'SOUTH'): ['RIGHT', 'RIGHT'],
        ('NORTH', 'WEST'): ['LEFT'], ('EAST', 'NORTH'): ['LEFT'], ('EAST', 'EAST'): [],
        ('EAST', 'SOUTH'): ['RIGHT'], ('EAST', 'WEST'): ['RIGHT', 'RIGHT'], ('SOUTH', 'NORTH'): ['RIGHT', 'RIGHT'],
        ('SOUTH', 'EAST'): ['LEFT'], ('SOUTH', 'SOUTH'): [], ('SOUTH', 'WEST'): ['RIGHT'],
        ('WEST', 'NORTH'): ['RIGHT'], ('WEST', 'EAST'): ['RIGHT', 'RIGHT'], ('WEST', 'SOUTH'): ['LEFT'],
        ('WEST', 'WEST'): []
    }
    SENSES = defaultdict(str, {'P': 'B', 'W': 'S', 'G': 'G'})

    def __init__(self, world_map, size):
        self.world_map = defaultdict(str, world_map)  # Map of the environment
        self.size = size  # Size of the environment
        self.knowledge_base = defaultdict(set)  # Knowledge base of the agent
        self.position = (1, 1)  # Initial position of the agent
        self.direction = 'EAST'  # Initial direction of the agent
        self.arrow_count = 1  # Number of arrows the agent has
        self.score = 0  # Initial score of the agent
        self.have_gold = 0  # Flag indicating if the agent has obtained gold
        self.is_alive = 1  # Flag indicating if the agent is alive

    def turn_left(self):
        """Turn the agent left"""
        self.score -= 1
        self.direction = Agent.LEFT[self.direction]
        print('Turned left')

    def turn_right(self):
        """Turn the agent right"""
        self.score -= 1
        self.direction = Agent.RIGHT[self.direction]
        print('Turned right')

    def move_forward(self):
        """Move the agent forward"""
        new_position = np.array(self.position) + np.array(Agent.FORWARD[self.direction])

        if any(coord < 1 or coord > self.size for coord in new_position):
            print('Hit wall at', self.position)
            return False

        self.score -= 1
        self.position = tuple(new_position)
        self.knowledge_base[self.position].add('V')  # Mark the current position as visited
        # Handle obstacles
        if self.world_map[self.position] in ('P', 'W'):
            self.is_alive = 0
            self.score -= 1000
            reason = 'pit' if self.world_map[self.position] == 'P' else 'wumpus'
            print('Died at', self.position, 'because of', reason)
            return False
        else:
            self.knowledge_base[self.position].add('OK')  # Mark the current position as safe
        print('Move forward to', self.position)
        return True

    def shoot(self):
        """Agent shoots an arrow"""
        print('Shoot arrow')
        if self.arrow_count:
            self.score -= 10
            self.arrow_count = 0
            new_position = np.array(self.position) + np.array(Agent.FORWARD[self.direction])
            if any(coord < 1 or coord > self.size for coord in new_position):
                return
            new_position = tuple(new_position)
            if self.world_map[new_position] == 'W':
                self.knowledge_base[new_position].add('Sc')  # Mark the wumpus as shot
                self.world_map.pop(new_position)
                print('Killed wumpus at', new_position)
            else:
                print('Missed at', new_position)
        else:
            print('No arrow')

    def grab(self):
        """Agent grabs the gold"""
        print('Grab gold')
        if self.world_map[self.position] == 'G':
            self.have_gold = 1
            self.score += 1000
            self.world_map.pop(self.position)
            print('Grabbed gold at', self.position)
        else:
            print('No gold at', self.position)

    def sense(self):
        """Agent senses its environment"""
        if self.world_map[self.position] == 'G':
            self.knowledge_base[self.position].add('G')  # Mark the gold as sensed
        all_environment = set()
        for adjacent_position in self.adjacent():
            environment = self.world_map[adjacent_position]
            all_environment.add(environment)
            if environment and environment != 'G':
                self.knowledge_base[self.position].add(Agent.SENSES[environment])  # Add sensed environment to KB
        if 'W' not in all_environment:
            self.knowledge_base[self.position].discard('S')  # Remove stench if wumpus not present
        return self.knowledge_base[self.position]

    def adjacent(self, position=None):
        """Get adjacent positions"""
        position = np.array(self.position) if position is None else np.array(position)
        adjacents = []
        for direction in Agent.FORWARD.values():
            new_position = position + np.array(direction)
            if all(1 <= coord <= self.size for coord in new_position):
                adjacents.append(tuple(new_position))
        return adjacents

    def __repr__(self):
        """Represent agent's state"""
        return f'Agent({self.position}, {self.direction})\nScore: {self.score}'

def move_to(agent, destination):
    """Move agent to the specified destination"""
    print('Go to', destination)
    destination_difference = tuple(np.array(destination) - np.array(agent.position))
    desired_direction = list(Agent.FORWARD.keys())[list(Agent.FORWARD.values()).index(destination_difference)]
    turns_required = Agent.TURNS[(agent.direction, desired_direction)]
    for turn in turns_required:
        if turn == 'LEFT':
            agent.turn_left()
        elif turn == 'RIGHT':
            agent.turn_right()
    agent.move_forward()

def ai_next_action(agent: Agent):
    """Determine the next action for the agent"""
    senses = agent.sense()
    print('Current:', {agent.position: agent.knowledge_base[agent.position]})
    print('Action:', end=' ')
    if 'G' in senses:
        agent.grab()
        return True
    ok_visited, ok_not_visited = [], []
    for adjacent_position in agent.adjacent():
        if 'W' in agent.knowledge_base[adjacent_position]:
            agent.shoot()
            return True
        if 'OK' in agent.knowledge_base[adjacent_position] and 'V' not in agent.knowledge_base[adjacent_position]:
            ok_not_visited.append(adjacent_position)
            continue
        if 'OK' in agent.knowledge_base[adjacent_position] and 'V' in agent.knowledge_base[adjacent_position]:
            ok_visited.append(adjacent_position)
    if ok_not_visited:
        move_to(agent, ok_not_visited[0])
        return True
    if ok_visited:
        move_to(agent, ok_visited[0])
        return True
    return False

def analyze_adjacent(agent: Agent):
    """Analyze the adjacent positions and update agent's knowledge base"""
    senses = agent.sense()
    agent.knowledge_base[agent.position].add('V')  # Mark current position as visited
    agent.knowledge_base[agent.position].add('OK')  # Mark current position as safe
    total_ok = 0
    adjacent_positions = agent.adjacent()
    print('Adjacent positions:', {adj: agent.knowledge_base[adj] for adj in adjacent_positions})
    for adj in adjacent_positions:
        # Infer potential hazards based on agent's senses
        if 'OK' not in agent.knowledge_base[adj] and 'P' not in agent.knowledge_base[adj] and 'W' not in agent.knowledge_base[adj]:
            if 'B' in senses and 'S' in senses:
                agent.knowledge_base[adj].add('P?')
                agent.knowledge_base[adj].add('W?')
            elif 'B' in senses:
                if 'W?' not in agent.knowledge_base[adj]:
                    agent.knowledge_base[adj].add('P?')
                agent.knowledge_base[adj].discard('W?')
            elif 'S' in senses:
                if 'P?' not in agent.knowledge_base[adj]:
                    agent.knowledge_base[adj].add('W?')
                agent.knowledge_base[adj].discard('P?')
            else:
                agent.knowledge_base[adj].discard('P?')
                agent.knowledge_base[adj].discard('W?')
        # Mark position as safe if no potential hazards detected
        if 'P?' not in agent.knowledge_base[adj] and 'W?' not in agent.knowledge_base[adj]:
            agent.knowledge_base[adj].add('OK')
            total_ok += 1
    # If all adjacent positions are safe except one, infer the type of hazard in that position
    if total_ok == len(adjacent_positions)-1:
        for adj in adjacent_positions:
            if 'OK' not in agent.knowledge_base[adj] and 'P' not in agent.knowledge_base[adj] and 'W' not in agent.knowledge_base[adj]:
                if 'B' in senses and 'P?' in agent.knowledge_base[adj]:
                    agent.knowledge_base[adj].add('P')
                    agent.knowledge_base[adj].discard('P?')
                    break
                elif 'S' in senses and 'W?' in agent.knowledge_base[adj]:
                    agent.knowledge_base[adj].add('W')
                    agent.knowledge_base[adj].discard('W?')
                    break

def user_traverse(agent: Agent):
    """Allow user to interact with the agent"""
    print('1. Move forward')
    print('2. Turn left')
    print('3. Turn right')
    print('4. Shoot')
    print('5. Grab')
    print('6. Exit')
    action = int(input('Enter action: '))
    while agent.is_alive:
        if agent.position == (1, 1) and agent.have_gold:
            print('You won!')
            break
        if action == 1:
            agent.move_forward()
            analyze_adjacent(agent)
        elif action == 2:
            agent.turn_left()
        elif action == 3:
            agent.turn_right()
        elif action == 4:
            agent.shoot()
        elif action == 5:
            agent.grab()
        elif action == 6:
            break
        action = int(input('Enter action: '))  # Prompt for next action

def ai_traverse(agent):
    """Allow the AI to traverse the environment"""
    path = []
    max_iterations = 100
    while agent.is_alive and not agent.have_gold and max_iterations > 0:
        print(agent)
        analyze_adjacent(agent)
        if not ai_next_action(agent):
            print('No action possible to take by AI')
            user_traverse(agent)
            return
        if agent.position in path:
            # Remove path until reaching a previously visited position to prevent looping
            path = path[:path.index(agent.position)]
        path.append(agent.position)
        max_iterations -= 1
        print()
    if not agent.is_alive:
        return
    if agent.have_gold:
        path.pop()
        while agent.position != (1, 1):
            print(agent)
            print('Action:', end=' ')
            move_to(agent, path.pop())
            print()
        print(agent)
        print('AI won!')
    if max_iterations == 0:
        print('Max iteration reached')
        user_traverse(agent)

def main():
    # Define the environment
    world_map = {
        (3, 1): 'P', (1, 3): 'W', (2, 3): 'G', (3, 3): 'P', (4, 4): 'P',
    }

    agent = Agent(world_map, 4)
    ai_traverse(agent)

if __name__ == '__main__':
    main()