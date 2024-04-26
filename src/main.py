import random

nodes_registry = {}
start_node = ''
end_node = ''

class Node:
    def __init__(self, name):
        """
        Initializes a Node with a given name, an empty routing table, and default traffic settings.
        
        :param name: The name of the node.
        """
        self.name = name
        self.routing_table = {}
        self.is_compromised = False
        self.traffic = 0
        nodes_registry[name] = self

    def update_routing_table(self, adjacent_node, cost):
        """
        Updates the routing table to add or modify the cost to an adjacent node.
        
        :param adjacent_node: The name of the adjacent node.
        :param cost: The cost to reach the adjacent node.
        """
        self.routing_table[adjacent_node] = cost

    def mark_as_compromised(self):
        """
        Marks the node as compromised, affecting the traffic routing decisions.
        """
        self.is_compromised = True

    def update_traffic(self, traffic):
        """
        Updates the traffic metric for this node.
        
        :param traffic: The amount of traffic currently going through the node.
        """
        self.traffic = traffic

class Chromosome:
    def __init__(self, node_sequence):
        """
        Initializes a Chromosome with a sequence of nodes and calculates its fitness.
        
        :param node_sequence: A sequence of nodes represented as a string.
        """
        self.node_sequence = node_sequence
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        """
        Calculates and returns the fitness of the chromosome based on the node sequence.
        
        :return: The fitness score as an integer.
        """
        return fitness_function(self.node_sequence)

def fitness_function(node_sequence):
    """
    Calculates the total cost of a given node sequence, taking into account routing costs, traffic, and node compromises.
    
    :param node_sequence: The sequence of nodes to evaluate.
    :return: The total cost as an integer, or None if any node in the sequence is not found.
    """
    total_cost = 0
    for i in range(len(node_sequence) - 1):
        current_node = node_sequence[i]
        next_node = node_sequence[i + 1]
        node_instance = nodes_registry.get(current_node)
        
        if node_instance:
            weight = 2
            total_cost += node_instance.routing_table.get(next_node, 0) + (node_instance.traffic * weight)
            if node_instance.is_compromised:
                total_cost += 100000
        else:
            print(f"Node {current_node} not found in registry.")
            return None
    return total_cost

def generate_valid_path(origin, destination):
    """
    Generates a random valid path from the origin node to the destination node.
    
    :param origin: The starting node of the path.
    :param destination: The ending node of the path.
    :return: A string representing the sequence of nodes in the path.
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
    Performs a genetic crossover between two parent chromosomes, ensuring valid paths are produced.
    
    :param parent1: The node sequence of the first parent.
    :param parent2: The node sequence of the second parent.
    :param origin: The origin node of the path.
    :param destination: The destination node of the path.
    :return: A tuple containing two Chromosomes representing the offspring.
    """
    if min(len(parent1), len(parent2)) <= 2:
        return (Chromosome(generate_valid_path(origin, destination)), Chromosome(generate_valid_path(origin, destination)))
    
    crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 2)
    offspring1_attempt = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2_attempt = parent2[:crossover_point] + parent1[crossover_point:]

    offspring1 = offspring1_attempt if is_valid_path(offspring1_attempt, origin, destination) else generate_valid_path(origin, destination)
    offspring2 = offspring2_attempt if is_valid_path(offspring2_attempt, origin, destination) else generate_valid_path(origin, destination)

    return Chromosome(offspring1), Chromosome(offspring2)

def is_valid_path(path, origin, destination):
    """
    Validates whether a given path is feasible from the origin to the destination node.
    
    :param path: The path to validate as a string.
    :param origin: The origin node of the path.
    :param destination: The destination node of the path.
    :return: True if the path is valid, False otherwise.
    """
    if path[0] != origin or path[-1] != destination:
        return False
    for i in range(len(path) - 1):
        if path[i+1] not in nodes_registry[path[i]].routing_table:
            return False
    return True

def main():
    # Main function logic here
    pass

if __name__ == "__main__":
    main()
