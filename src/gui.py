import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import main  # Import your main module

# Create the main window
root = tk.Tk()
root.title("Network Pathfinding Simulation")

# Frame for network graph
frame_graph = tk.Frame(root)
frame_graph.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Frame for controls
frame_controls = tk.Frame(root)
frame_controls.pack(side=tk.RIGHT, fill=tk.Y)

# NetworkX graph
G = nx.DiGraph()

# Function to add nodes to the graph and update the node registry
def add_node(node_name):
    if node_name and node_name not in G.nodes:
        G.add_node(node_name)
        main.Node(node_name)  # Create a Node instance
        update_graph()
    else:
        messagebox.showerror("Error", "Node already exists or invalid name.")

# Function to add edges to the graph and update the routing tables
def add_edge():
    node1 = node1_entry.get()
    node2 = node2_entry.get()
    try:
        weight = int(weight_entry.get())
        if node1 and node2 and node1 in G.nodes and node2 in G.nodes and node1 != node2:
            G.add_edge(node1, node2, weight=weight)
            main.nodes_registry[node1].update_routing_table(node2, weight)
            main.nodes_registry[node2].update_routing_table(node1, weight)  # Assuming bidirectional
            update_graph()
        else:
            messagebox.showerror("Error", "Invalid node names or weight.")
    except ValueError:
        messagebox.showerror("Error", "Invalid weight.")

# Function to draw or update the graph
def update_graph(highlight_path=None):
    """
    Draw or update the network graph with optional path highlighting.
    
    :param highlight_path: str - A string representing the sequence of nodes in the fittest path to highlight.
    """
    ax.clear()  # Clear the previous graph drawing
    pos = nx.spring_layout(G)  # Positions for all nodes

    # Default node and edge colors
    node_color_map = []
    edge_color_map = []

    for node in G.nodes():
        if highlight_path and node in highlight_path:
            node_color_map.append('green')
        else:
            node_color_map.append('skyblue')

    for u, v in G.edges():
        if highlight_path and u in highlight_path and v in highlight_path and \
           highlight_path.index(v) == highlight_path.index(u) + 1:
            edge_color_map.append('green')
        else:
            edge_color_map.append('black')

    nx.draw(G, pos, ax=ax, with_labels=True, node_color=node_color_map, node_size=2000,
            edge_color=edge_color_map, linewidths=1, font_size=15)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
    canvas.draw()
    
sequences = []
for i in range(6):
    sequences.append(main.generate_valid_path(main.start_node, main.end_node))

chromosomes = [main.Chromosome(seq) for seq in sequences]

        
def genetic_mainloop(delay=1000):  # Delay in milliseconds
    main.end_node = end_node_entry.get()
    main.start_node = start_node_entry.get()
    
    # sequences = []
    # for i in range(6):
    #     sequences.append(main.generate_valid_path(main.start_node, main.end_node))
    
    print(f"start node : {main.start_node} end node : {main.end_node} ")
    print(sequences)
    
    # chromosomes = [main.Chromosome(seq) for seq in sequences]
    chromosomes_sorted_by_fitness = sorted(chromosomes, key=lambda x: x.fitness)
    fittest_chromosome = chromosomes_sorted_by_fitness[0]
    
    print(fittest_chromosome.node_sequence) # printing empty sequence
    
    update_graph(highlight_path=fittest_chromosome.node_sequence)
    
    parent1, parent2 = chromosomes_sorted_by_fitness[:2]        
    chromosomes = []
    for w in range(0, 3):
        offspring1, offspring2 = main.crossover_with_validation(parent1.node_sequence, parent2.node_sequence, main.start_node, main.end_node)
        chromosomes.append(offspring1)
        chromosomes.append(offspring2)

    # Schedule the next call to this function
    root.after(delay, genetic_mainloop, delay)
    
# Adding node entry
ttk.Label(frame_controls, text="Node Name:").pack()
node_entry = ttk.Entry(frame_controls)
node_entry.pack()
ttk.Button(frame_controls, text="Add Node", command=lambda: add_node(node_entry.get())).pack()

# Adding edges
ttk.Label(frame_controls, text="Node 1:").pack()
node1_entry = ttk.Entry(frame_controls)
node1_entry.pack()
ttk.Label(frame_controls, text="Node 2:").pack()
node2_entry = ttk.Entry(frame_controls)
node2_entry.pack()
ttk.Label(frame_controls, text="Weight:").pack()
weight_entry = ttk.Entry(frame_controls)
weight_entry.pack()
ttk.Button(frame_controls, text="Add Edge", command=add_edge).pack()

# Entry for start and end nodes
ttk.Label(frame_controls, text="Start Node:").pack()
start_node_entry = ttk.Entry(frame_controls)
start_node_entry.pack()

ttk.Label(frame_controls, text="End Node:").pack()
end_node_entry = ttk.Entry(frame_controls)
end_node_entry.pack()

ttk.Button(frame_controls, text="Start Genetic Algorithm", command=lambda: genetic_mainloop(1000)).pack()

# Matplotlib figure and axis
fig: Figure = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root.mainloop()
