import random
import copy

nodes_registry = {}

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

# Example usage (commented out to follow instructions)
# node_a = Node("NodeA")
# node_a.update_routing_table("NodeB", 2)
# node_a.update_routing_table("NodeC", 5)
# node_a.mark_as_compromised()
# node_a.update_traffic(100)

# print(node_a.name, node_a.routing_table, node_a.is_compromised, node_a.traffic)

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

# Example usage (commented out to follow instructions)
# Assume nodes_registry is populated and fitness_function is defined as before.
# chromosome = Chromosome("ACDEF")
# print(chromosome.node_sequence, chromosome.fitness)


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

def repair_route(route, origin, destination):
    """
    Repair a route to ensure it starts at the origin and ends at the destination without repetitions.
    
    :param route: list - The sequence of nodes.
    :param origin: str - The origin node.
    :param destination: str - The destination node.
    :return: list - The repaired sequence of nodes.
    """
    # Ensure route starts with origin and ends with destination
    route_list = list(route)  # Convert string to list
    
    if route_list[0] != origin:
        route_list.insert(0, origin)
    if route_list[-1] != destination:
        route_list.append(destination)
    
    seen = set([origin])
    repaired_route = [origin]
    for node in route_list[1:-1]:
        if node not in seen and node != destination:
            repaired_route.append(node)
            seen.add(node)
    repaired_route.append(destination)
    
    return ''.join(repaired_route)  # Convert list back to string

# Correcting the crossover function to use the fixed repair_route
def crossover_chromosomes(parent1, parent2, origin, destination):
    route1 = copy.deepcopy(parent1.node_sequence)
    route2 = copy.deepcopy(parent2.node_sequence)

    if min(len(route1), len(route2)) > 2 and route1 != route2:
        if min(len(route1), len(route2)) == 3:
            crossover_point = random.randint(1, min(len(route1), len(route2)) - 1)
            offspring1_route = route1 + route2[crossover_point:]
            offspring2_route = route2 + route1[crossover_point:]
        else:
            crossover_point = random.randint(2, min(len(route1), len(route2)) - 2)
            offspring1_route = route1[:crossover_point] + route2[crossover_point:]
            offspring2_route = route2[:crossover_point] + route1[crossover_point:]

        offspring1_route = repair_route(offspring1_route, origin, destination)
        offspring2_route = repair_route(offspring2_route, origin, destination)

        offspring1 = Chromosome("".join(offspring1_route))
        offspring2 = Chromosome("".join(offspring2_route))

        return offspring1, offspring2
    else:
        return parent1, parent2

# Assuming the rest of the setup (Chromosome class, nodes_registry) is as previously defined.

def main():
    # Step 1: Create a medium complexity network
    nodes = ['A', 'B', 'C', 'D', 'E', 'F']
    connections = {
        ('A', 'B'): 4, ('A', 'C'): 3,
        ('B', 'C'): 2, ('B', 'D'): 5,
        ('C', 'D'): 3, ('C', 'E'): 4,
        ('D', 'E'): 2, ('D', 'F'): 3,
        ('E', 'F'): 5
    }
    for node in nodes:
        Node(node)
    for (start, end), cost in connections.items():
        nodes_registry[start].update_routing_table(end, cost)
        # For simplicity, assume all connections are bidirectional
        nodes_registry[end].update_routing_table(start, cost)

    # Randomly mark one node as compromised and one with high traffic
    # nodes_registry[random.choice(nodes)].is_compromised = True
    # nodes_registry[random.choice(nodes)].traffic = 100

    # Step 2: Create 5 random sequences of valid routes
    sequences = ['ABCDEF', 'AFEDCB', 'AEDCFB', 'ABCDE', 'AFDEC']
    chromosomes = [Chromosome(seq) for seq in sequences]

    # Step 3: Calculate fitness and print
    for i, chromosome in enumerate(chromosomes, start=1):
        print(f"Chromosome {i}: Sequence {chromosome.node_sequence}, Fitness {chromosome.fitness}")

    # Step 4: Perform crossover on two randomly selected chromosomes
    parents = random.sample(chromosomes, 2)
    print(f"The chosen parents are : {parents[0].node_sequence}, {parents[1].node_sequence}")
    offspring1, offspring2 = crossover_chromosomes(parents[0], parents[1], 'A', 'F')
    print(f"Offspring 1: Sequence {offspring1.node_sequence}, Fitness {offspring1.fitness}")
    print(f"Offspring 2: Sequence {offspring2.node_sequence}, Fitness {offspring2.fitness}")

# To run the main function, uncomment the next line in your Python environment
# main()

if __name__ == "__main__":
    main()