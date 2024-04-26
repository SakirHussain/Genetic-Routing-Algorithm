import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import main  # Import the main module containing the logic

# Create the main window
root = tk.Tk()
root.title("Network Pathfinding Simulation")

# Frame for network graph
frame_graph = tk.Frame(root)
frame_graph.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Frame for controls
frame_controls = tk.Frame(root)
frame_controls.pack(side=tk.RIGHT, fill=tk.Y)

# NetworkX graph initialization
G = nx.DiGraph()
pos = {}  # Positions for all nodes

def add_node(node_name):
    """
    Adds a node to the graph and updates the node registry.

    :param node_name: The name of the node to be added.
    """
    global pos
    if node_name and node_name not in G.nodes:
        G.add_node(node_name)
        main.Node(node_name)  # Create a Node instance
        pos = nx.spring_layout(G)  # Recalculate layout only when new nodes are added
        update_graph()
    else:
        messagebox.showerror("Error", "Node already exists or invalid name.")

def add_edge():
    """
    Adds an edge between two nodes with specified weight and updates routing tables.
    """
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

def update_graph(highlight_path=None):
    """
    Draws or updates the network graph with optional path highlighting.

    :param highlight_path: A list of node names representing the path to highlight.
    """
    ax.clear()  # Clear the previous graph drawing
    node_color_map = ['green' if highlight_path and node in highlight_path else 'skyblue' for node in G.nodes()]
    edge_color_map = ['green' if highlight_path and u in highlight_path and v in highlight_path and
                      highlight_path.index(v) == highlight_path.index(u) + 1 else 'black' for u, v in G.edges()]
    
    nx.draw(G, pos, ax=ax, with_labels=True, node_color=node_color_map, node_size=2000,
            edge_color=edge_color_map, linewidths=1, font_size=15)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
    canvas.draw()
    fig.canvas.mpl_connect('button_press_event', on_click)

def on_click(event):
    """
    Handles click events on the graph to identify which node was clicked.

    :param event: The event data.
    """
    node_clicked = None
    for node, (x, y) in pos.items():
        distance = ((event.xdata - x)**2 + (event.ydata - y)**2)**0.5
        if distance < 0.1:  # Threshold to detect a node click
            node_clicked = node
            break

    if node_clicked:
        print(f"Node {node_clicked} was clicked.")  # Debug: to be replaced with actual functionality
        show_node_controls(node_clicked)

node_controls_frame = tk.Frame(frame_controls)
node_controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

def show_node_controls(node_name):
    """
    Displays control widgets for a specific node for editing its properties.

    :param node_name: The name of the node being edited.
    """
    for widget in node_controls_frame.winfo_children():
        widget.destroy()

    ttk.Label(node_controls_frame, text=f"Editing Node: {node_name}").pack()
    is_comp_var = tk.BooleanVar(value=main.nodes_registry[node_name].is_compromised)
    compromised_check = ttk.Checkbutton(node_controls_frame, text="Is Compromised", variable=is_comp_var, 
                                        command=lambda: update_node_compromised(node_name, is_comp_var))
    compromised_check.pack()

    traffic_var = tk.IntVar(value=main.nodes_registry[node_name].traffic)
    ttk.Label(node_controls_frame, text="Traffic Level:").pack()
    traffic_entry = ttk.Entry(node_controls_frame, textvariable=traffic_var)
    traffic_entry.pack()
    update_traffic_btn = ttk.Button(node_controls_frame, text="Update Traffic",
                                    command=lambda: update_node_traffic(node_name, traffic_var.get()))
    update_traffic_btn.pack()

def update_node_compromised(node_name, is_compromised):
    """
    Updates the compromised status of a node and refreshes the graph.

    :param node_name: The node whose status is to be updated.
    :param is_compromised: The new compromised status as a BooleanVar.
    """
    node = main.nodes_registry[node_name]
    node.is_compromised = is_compromised.get()
    update_graph()  # Refresh the graph

def update_node_traffic(node_name, traffic):
    """
    Updates the traffic level for a specific node and triggers graph refresh and genetic algorithm restart.
    
    :param node_name: The name of the node to update.
    :param traffic: The new traffic level for the node.
    """
    node = main.nodes_registry[node_name]
    node.traffic = traffic
    update_graph()  # Refresh the graph
    restart_genetic_algorithm()

def restart_genetic_algorithm():
    """
    Restarts the genetic algorithm, cancelling any existing schedules and setting a new one.
    """
    global chromosomes, genetic_algorithm_job
    if genetic_algorithm_job is not None:
        root.after_cancel(genetic_algorithm_job)
    genetic_mainloop(setup_initial_population(), 1000)  # Restart with a standard delay

chromosomes = []
def setup_initial_population():
    """
    Sets up the initial population for the genetic algorithm based on configured start and end nodes.
    
    :return: A list of Chromosome objects representing the initial population.
    """
    main.end_node = end_node_entry.get()
    main.start_node = start_node_entry.get()
    sequences = ['ABCDEDCDEF', 'ACBDEDCEDEF', 'ABCEDEDCBDF', 'ACDEDCEDCEF', 'ACBCDCEDEDF']
    chromosomes = [main.Chromosome(seq) for seq in sequences]
    return chromosomes

genetic_algorithm_job = None
def genetic_mainloop(chromosomes, delay=1000):
    """
    Continuously runs the genetic algorithm, evolving the population at specified intervals.
    
    :param chromosomes: The current population of chromosomes.
    :param delay: The delay (in milliseconds) between evolution steps.
    """
    global genetic_algorithm_job
    main.end_node = end_node_entry.get()
    main.start_node = start_node_entry.get()
    print(f"Start node: {main.start_node}, End node: {main.end_node}")
    
    chromosomes_sorted_by_fitness = sorted(chromosomes, key=lambda x: x.fitness)
    fittest_chromosome = chromosomes_sorted_by_fitness[0]
    
    for i in chromosomes_sorted_by_fitness:
        print(f"Node sequence: {i.node_sequence}, Fitness: {i.fitness}")
    
    print("Fittest chromosome node sequence:", fittest_chromosome.node_sequence)
    update_graph(highlight_path=fittest_chromosome.node_sequence)
    
    parent1, parent2 = chromosomes_sorted_by_fitness[:2]
    chromosomes = []
    for _ in range(3):
        offspring1, offspring2 = main.crossover_with_validation(parent1.node_sequence, parent2.node_sequence, main.start_node, main.end_node)
        chromosomes.append(offspring1)
        chromosomes.append(offspring2)

    if genetic_algorithm_job is not None:
        root.after_cancel(genetic_algorithm_job)

    genetic_algorithm_job = root.after(delay, lambda: genetic_mainloop(chromosomes, delay))

# User interface for adding nodes and edges
ttk.Label(frame_controls, text="Node Name:").pack()
node_entry = ttk.Entry(frame_controls)
node_entry.pack()
ttk.Button(frame_controls, text="Add Node", command=lambda: add_node(node_entry.get())).pack()

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

# Entry fields for configuring start and end nodes for the genetic algorithm
ttk.Label(frame_controls, text="Start Node:").pack()
start_node_entry = ttk.Entry(frame_controls)
start_node_entry.pack()
ttk.Label(frame_controls, text="End Node:").pack()
end_node_entry = ttk.Entry(frame_controls)
end_node_entry.pack()

# Button to start the genetic algorithm
ttk.Button(frame_controls, text="Start Genetic Algorithm", command=lambda: genetic_mainloop(setup_initial_population(), 1000)).pack()

# Setup for displaying the network graph
fig: Figure = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root.mainloop()
