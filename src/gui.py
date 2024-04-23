import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
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
def update_graph():
    ax.clear()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, ax=ax, with_labels=True, node_color='skyblue', node_size=2000, edge_color='k', linewidths=1, font_size=15)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
    canvas.draw()

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

# Matplotlib figure and axis
fig: Figure = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root.mainloop()
