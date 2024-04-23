import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

# Function to add nodes to the graph
def add_node(node):
    G.add_node(node)
    draw_graph()

# Function to add edges to the graph
def add_edge(edge_info):
    try:
        nodes, weight = edge_info.split('(')
        node1, node2 = nodes.split('-')
        weight = int(weight.rstrip(')'))
        G.add_edge(node1, node2, weight=weight)
        draw_graph()
    except Exception as e:
        print("Error adding edge:", e)

# Function to draw or update the graph
def draw_graph():
    ax.clear()
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, pos, ax=ax, with_labels=True, node_color='skyblue', node_size=2000, edge_color='k', linewidths=1, font_size=15)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
    canvas.draw()

# Adding node entry
node_label = ttk.Label(frame_controls, text="Add Node:")
node_label.pack()
node_entry = ttk.Entry(frame_controls)
node_entry.pack()

# Adding edges
edge_label = ttk.Label(frame_controls, text="Add Edge From-To (Weight):")
edge_label.pack()
edge_entry = ttk.Entry(frame_controls)
edge_entry.pack()

# Buttons for adding nodes and edges
add_node_button = ttk.Button(frame_controls, text="Add Node", command=lambda: add_node(node_entry.get()))
add_node_button.pack()
add_edge_button = ttk.Button(frame_controls, text="Add Edge", command=lambda: add_edge(edge_entry.get()))
add_edge_button.pack()

# Matplotlib figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=frame_graph)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root.mainloop()
