import random
import copy

nodes_registry = {}
start_node = ''
end_node = ''

class Node:
    def __init__(self, name):
        """
        Initialize a new Node instance.
        
        :param name: str - The name of the node.
        """
        self.name = name
        self.routing_table = {}
        self.is_compromised = False
        self.traffic = 0
        nodes_registry[name] = self


    def update_routing_table(self, adjacent_node, cost):
        """
        Update the routing table with the cost to an adjacent node.
        
        :param adjacent_node: str - The name of the adjacent node.
        :param cost: int - The cost to reach the adjacent node.
        """
        self.routing_table[adjacent_node] = cost

    def mark_as_compromised(self):
        """
        Mark the node as compromised.
        """
        self.is_compromised = True

    def update_traffic(self, traffic):
        """
        Update the traffic through the node.
        
        :param traffic: int - The amount of traffic.
        """
        self.traffic = traffic


class Chromosome:
    def __init__(self, node_sequence):
        """
        Initialize a Chromosome instance with a node sequence.
        
        :param node_sequence: str - A string representing a sequence of nodes.
        """
        self.node_sequence = node_sequence
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        """
        Calculate and return the fitness of the node sequence.
        
        :return: int - The fitness value of the node sequence.
        """
        return fitness_function(self.node_sequence)


def fitness_function(node_sequence):
    """
    Calculate the overall cost of the given node sequence.
    
    :param node_sequence: str - A string representing a sequence of nodes.
    :return: int - The overall cost of traversing the nodes in the given sequence.
    """
    total_cost = 0
    for i in range(len(node_sequence) - 1):
        current_node = node_sequence[i]
        next_node = node_sequence[i + 1]
        
        # Lookup the current Node instance
        node_instance = nodes_registry.get(current_node)
        if node_instance:
            weight = 2
            # Add the cost to the total if the next node is in the current node's routing table
            total_cost += node_instance.routing_table.get(next_node, 0) + (node_instance.traffic * weight)
            if(node_instance.is_compromised):
                total_cost += 100000
            
        else:
            print(f"Node {current_node} not found in registry.")
            return None  # or some error handling
    
    return total_cost


def generate_valid_path(origin, destination):
    """
    Generate a valid path from origin to destination.
    This is a placeholder function that should implement a pathfinding algorithm like Dijkstra or BFS.
    """
    path = [origin]
    current_node = origin
    while current_node != destination:
        next_nodes = list(nodes_registry[current_node].routing_table.keys())
        if not next_nodes:
            raise ValueError("No path found")
        next_node = random.choice(next_nodes)
        path.append(next_node)
        current_node = next_node
    return "".join(path)

def crossover_with_validation(parent1, parent2, origin, destination):
    """
    Perform crossover between two parent strings ensuring the offspring is a valid path.
    """
    if min(len(parent1), len(parent2)) <= 2:
        # If either parent is too short, we simply generate new paths
        offspring1 = generate_valid_path(origin, destination)
        offspring2 = generate_valid_path(origin, destination)
        return (Chromosome(offspring1),
                Chromosome(offspring2))
    
    # Simple crossover: mix and match halves
    crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 2)
    offspring1_attempt = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2_attempt = parent2[:crossover_point] + parent1[crossover_point:]

    # Validate offspring paths; if not valid, generate a new valid path
    offspring1 = offspring1_attempt if is_valid_path(offspring1_attempt, origin, destination) else generate_valid_path(origin, destination)
    offspring2 = offspring2_attempt if is_valid_path(offspring2_attempt, origin, destination) else generate_valid_path(origin, destination)

    return Chromosome(offspring1), Chromosome(offspring2)

def is_valid_path(path, origin, destination):
    """
    Check if a given path string is valid from origin to destination.
    """
    if path[0] != origin or path[-1] != destination:
        return False
    for i in range(len(path) - 1):
        if path[i+1] not in nodes_registry[path[i]].routing_table:
            return False
    return True


def main():
    # # Step 1: Create a medium complexity network
    # nodes = ['A', 'B', 'C', 'D', 'E', 'F']
    # connections = {
    #     ('A', 'B'): 4, ('A', 'C'): 3,
    #     ('B', 'C'): 2, ('B', 'D'): 5,
    #     ('C', 'D'): 3, ('C', 'E'): 4,
    #     ('D', 'E'): 2, ('D', 'F'): 3,
    #     ('E', 'F'): 5
    # }
    
    # for node in nodes:
    #     Node(node)
        
    # for (start, end), cost in connections.items():
    #     nodes_registry[start].update_routing_table(end, cost)
    #     # For simplicity, assume all connections are bidirectional
    #     nodes_registry[end].update_routing_table(start, cost)

    
    # Step 2: Create 5 random sequences of valid routes
    
    
    # sequences = ['ABCDEDCDEF', 'ACBDEDCEDEF', 'ABCEDEDCBDF', 'ACDEDCEDCEF', 'ACBCDCEDEDF']
    
    # chromosomes = [Chromosome(seq) for seq in sequences]

    for q in range(0, 10):    
    # Step 3: Calculate fitness and print
        for i, chromosome in enumerate(chromosomes, start=1):
            print(f"Chromosome {i}: Sequence {chromosome.node_sequence}, Fitness {chromosome.fitness}")

        chromosomes_sorted_by_fitness = sorted(chromosomes, key=lambda x: x.fitness)
        # Select the two chromosomes with the lowest fitness values
        parent1, parent2 = chromosomes_sorted_by_fitness[:2]        
        print(f"The chosen parents are : {parent1.node_sequence}, {parent2.node_sequence}")
        
        chromosomes = []
        for w in range(0, 3):
            offspring1, offspring2 = crossover_with_validation(parent1.node_sequence, parent2.node_sequence, 'A', 'F')    
            print(f"Offspring 1: Sequence {offspring1.node_sequence}, Fitness {offspring1.fitness}")
            print(f"Offspring 2: Sequence {offspring2.node_sequence}, Fitness {offspring2.fitness}\n")
            chromosomes.append(offspring1)
            chromosomes.append(offspring2)
        

# To run the main function, uncomment the next line in your Python environment
# main()

if __name__ == "__main__":
    main()