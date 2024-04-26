# Network Pathfinding Simulation

This project provides a graphical interface and backend logic to simulate and visualize network pathfinding using genetic algorithms. The system includes functionality to manage network nodes, adjust node properties, and dynamically update routes based on network changes.

## Installation

To run this software, ensure you have Python installed along with the necessary libraries. Here are the steps to set up the environment:

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### Required Libraries

- `tkinter`
- `NetworkX`
- `matplotlib`

You can install the required Python libraries using pip


Note: Tkinter comes pre-installed with most Python distributions. If it's not installed, refer to the Python documentation on how to install Tkinter for your operating system.

## Usage

To start the simulation, run the main Python script: `gui.py`



This will open a GUI where you can interact with the network simulation.

## Main Features

- **Add/Remove Nodes and Edges:** Dynamically add or remove nodes and edges from the network graph.
- **Adjust Node Properties:** Set nodes as compromised and adjust traffic levels through an interactive interface.
- **Visualization:** View the network graph with changes reflected in real-time, including path highlighting based on genetic algorithm results.
- **Genetic Algorithm Control:** Start, stop, and restart the genetic algorithm simulation to find optimal routing paths.

## Components

1. **Node Management:**
   - Nodes can be added or removed from the network graph. Each node's properties such as traffic level and compromised status can be manipulated.

2. **Edge Management:**
   - Edges between nodes can be added with specified weights, representing the cost or difficulty of traversal.

3. **Graph Visualization:**
   - The network is visualized using matplotlib and NetworkX, integrated within the Tkinter GUI.

4. **Genetic Algorithm:**
   - A genetic algorithm is implemented to optimize routing paths between nodes. This includes functions for crossover, mutation, and fitness evaluation based on path cost, traffic, and security status of nodes.

5. **GUI:**
   - A graphical user interface built with Tkinter allows interactive management of the network and visualization settings.

## File Structure

- `main.py`: Contains the backend logic including node and chromosome classes, and genetic algorithm functions.
- `gui.py`: Contains the Tkinter GUI setup, event handling, and integration with the NetworkX graph.