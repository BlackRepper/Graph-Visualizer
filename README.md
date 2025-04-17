# Graph-Visualizer

Understanding the Graph Visualizer Code (for Beginners)
This document explains the Python code used to create the DFS/BFS Graph Traversal Visualizer application using the Tkinter library.
1. Imports
import tkinter as tk
from tkinter import ttk, font
import time # Not directly used for delays, but good practice to know
from collections import deque


tkinter: This is Python's standard built-in library for creating Graphical User Interfaces (GUIs). We import the main library as tk.
tkinter.ttk: This submodule provides access to newer, themed widgets (like nicer-looking buttons and comboboxes) which generally look better across different operating systems.
tkinter.font: Used here specifically to make the node labels bold (font.Font(weight='bold')).
collections.deque: This provides a deque (double-ended queue) object. It's very efficient for adding and removing items from both ends, making it perfect for implementing the queue needed for the Breadth-First Search (BFS) algorithm.
2. Constants
# --- Constants ---
NODE_RADIUS = 20
# ... (other constants like colors, sizes, delay) ...
DELAY_MS = 700 # Delay between visualization steps in milliseconds


Constants are variables whose values ideally don't change once set. Using constants (often named in ALL_CAPS) makes the code easier to read and modify. If you want to change the node size or a color everywhere, you only need to change it in one place here.
NODE_RADIUS, CANVAS_WIDTH, CANVAS_HEIGHT, etc., define the visual dimensions.
NODE_COLOR_DEFAULT, NODE_COLOR_VISITING, etc., define the colors used during visualization.
DELAY_MS: This is crucial for the visualization. It sets the pause time (in milliseconds) between steps of the algorithm, allowing you to see the process unfold.
3. Graph Data
# --- Graph Data (Fixed) ---
graph = {
    'A': ['B', 'C', 'D'],
    # ... more nodes
}

# --- Node Positions (Fixed for layout) ---
node_positions = {
    'A': (CANVAS_WIDTH // 2, 50),
    # ... positions for other nodes
}


graph (Adjacency List): This dictionary represents the connections in our graph.
Each key (like 'A') is a node.
The value associated with each key (like ['B', 'C', 'D']) is a list of nodes that are directly connected to it (its neighbors). This way of representing graphs is called an adjacency list.
node_positions: This dictionary stores the (x, y) coordinates for drawing each node on the canvas. This provides a fixed, predefined layout for the graph visualization.
4. Pseudo Code
# --- Pseudo Code ---
DFS_CODE = [ ... list of strings ... ]
BFS_CODE = [ ... list of strings ... ]


These are simply lists of strings. Each string represents a line of pseudo-code (a simplified, human-readable description of an algorithm). These lists are used to display the steps of the selected algorithm in the text box on the left side of the application window.
5. The GraphVisualizerApp Class
class GraphVisualizerApp:
    # ... methods inside the class ...


In Python, a class is like a blueprint for creating objects. It bundles data (variables, called attributes) and functions (called methods) that operate on that data. Our entire application's logic and components are organized within this class.
5.1. __init__(self, master) (The Constructor)
    def __init__(self, master):
        self.master = master # 'master' is the main window
        # ... setup window title, size ...
        # ... setup style ...
        # ... initialize variables (node_objects, edge_objects, etc.) ...
        # ... create frames (left_frame, right_frame) ...
        # ... create widgets (buttons, labels, comboboxes, canvas, text area) ...
        # ... place widgets using pack() and grid() ...
        self.draw_graph()
        self.update_code_display()


__init__ is a special method called automatically when you create an instance of the class ( app = GraphVisualizerApp(root) at the bottom). It's used for initialization.
self: Represents the instance of the class itself. You use self. to access the object's attributes and methods from within the class.
master: This is the main Tkinter window (tk.Tk()) passed in when the app is created.
Key Actions:
Sets up the main window (title, geometry).
Initializes dictionaries (self.node_objects, self.edge_objects) to keep track of the shapes drawn on the canvas.
Creates GUI elements (widgets) like ttk.Button, ttk.Combobox, tk.Canvas, tk.Text.
Arranges these widgets in the window using layout managers (pack and grid).
Calls self.draw_graph() to draw the initial state of the graph.
Calls self.update_code_display() to show the default pseudo-code (DFS).
5.2. Drawing Functions (draw_graph, update_node_color, update_edge_color)
    def draw_graph(self):
        # ... clear canvas ...
        # ... draw edges (using create_line) ...
        # ... draw nodes (using create_oval and create_text) ...

    def update_node_color(self, node, color):
        # ... find the node's oval ID ...
        self.canvas.itemconfig(oval_id, fill=color) # Change color
        self.master.update() # IMPORTANT: Refresh the display

    # update_edge_color is similar for lines


These methods interact directly with the tk.Canvas widget.
draw_graph: Clears anything existing on the canvas (self.canvas.delete("all")) and then draws all the edges (create_line) and nodes (create_oval, create_text) based on the graph and node_positions data. It stores the unique IDs returned by the canvas creation methods in the self.node_objects, self.text_objects, and self.edge_objects dictionaries so we can refer to them later (e.g., to change their color).
update_node_color/update_edge_color: These methods take a node (or edge) and a color, find the corresponding shape's ID on the canvas using the stored dictionaries, and use self.canvas.itemconfig() to change its appearance (e.g., the fill color).
self.master.update(): This is called after changing an item's color to force Tkinter to immediately redraw that part of the screen. This makes the color change visible instantly during the visualization.
5.3. Code Highlighting (update_code_display, highlight_code_line)
    def update_code_display(self, event=None):
        # ... clear the text widget ...
        # ... get the selected algorithm (DFS or BFS) ...
        # ... insert the corresponding pseudo-code lines ...

    def highlight_code_line(self, line_index):
        # ... remove previous highlight (using tag_remove) ...
        # ... add highlight to the new line (using tag_add) ...
        self.master.update() # Refresh display


These methods manage the pseudo-code display area (tk.Text widget).
update_code_display: Clears the text box and fills it with the lines from either DFS_CODE or BFS_CODE based on the dropdown selection.
highlight_code_line: Uses Tkinter Text widget "tags". A tag named "highlight" is configured with a background color. This method first removes the tag from the previously highlighted line (if any) and then applies the tag to the specified line_index, making that line appear highlighted.
5.4. Visualization Logic (run_visualization, visualize_dfs, visualize_bfs, enable_controls)
    def run_visualization(self):
        # ... disable buttons, reset colors ...
        if algo == "DFS":
            self.visualize_dfs(start_node_val)
        else: # BFS
            self.visualize_bfs(start_node_val)
        # ... schedule enable_controls using self.master.after ...

    def visualize_dfs(self, start_node):
        # ... setup stack, visited set ...
        while stack:
            # ... algorithm step (e.g., node = stack.pop()) ...
            self.highlight_code_line(...) # Highlight corresponding code
            self.master.after(DELAY_MS)   # <<<< PAUSE HERE
            # ... check if visited ...
            self.highlight_code_line(...)
            self.master.after(DELAY_MS)   # <<<< PAUSE HERE
            if node not in visited:
                self.update_node_color(node, NODE_COLOR_VISITING) # Update visuals
                self.highlight_code_line(...)
                self.master.after(DELAY_MS)   # <<<< PAUSE HERE
                # ... more algorithm steps & visualization calls ...

    # visualize_bfs is similar but uses a queue (deque)

    def enable_controls(self):
        # ... re-enable buttons ...


This is the core of the application's functionality.
run_visualization: Called when the "Run" button is pressed. It disables the buttons (to prevent multiple runs at once), resets the graph's visual state, gets the selected algorithm and start node, and then calls either visualize_dfs or visualize_bfs. It uses self.master.after() to schedule the enable_controls method to run after the visualization is expected to finish.
visualize_dfs/visualize_bfs: These methods implement the actual DFS and BFS algorithms.
Key Concept: Instead of running the whole algorithm instantly, they interleave the algorithm's logical steps (like adding to a stack/queue, checking visited) with calls to:
self.highlight_code_line(): To show which step is being executed.
self.update_node_color()/self.update_edge_color(): To update the graph display.
self.master.after(DELAY_MS): This is the most important part for visualization in Tkinter. It tells Tkinter "wait for DELAY_MS milliseconds, then continue executing the next part of this function". This creates the pause needed to see each step without freezing the entire application window (which time.sleep() would do).
enable_controls: Simply re-enables the "Run" and "Reset" buttons after the visualization completes.
5.5. Reset Function (reset_visualization)
    def reset_visualization(self, clear_code_highlight=True):
        # ... loop through nodes and reset color using itemconfig ...
        # ... loop through edges and reset color using itemconfig ...
        # ... optionally clear code highlight ...
        self.master.update()


Called by the "Reset" button or at the beginning of run_visualization.
It iterates through all the stored node and edge objects and uses self.canvas.itemconfig() to set their colors back to the default ("lightblue" for nodes, "gray" for edges).
It also removes any active code highlighting.
6. Main Execution Block
# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()             # Create the main application window
    app = GraphVisualizerApp(root) # Create an instance of our app class
    root.mainloop()            # Start the Tkinter event loop


if __name__ == "__main__":: This is a standard Python pattern. Code inside this block only runs when the script is executed directly (not when it's imported as a module into another script).
root = tk.Tk(): Creates the main top-level window for the application.
app = GraphVisualizerApp(root): Creates an object (instance) of our GraphVisualizerApp class, passing the main window (root) to its __init__ method. This builds and sets up all the GUI elements.
root.mainloop(): Starts the Tkinter event loop. This makes the window appear on the screen and listens for events (like button clicks, mouse movements, key presses) and responds to them according to how the application is programmed. The program stays in this loop until the window is closed.
This breakdown should give you a good overview of how the different parts of the code work together to create the interactive graph visualizer.
