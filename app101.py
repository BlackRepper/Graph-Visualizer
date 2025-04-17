import tkinter as tk
from tkinter import ttk, font
import time
from collections import deque

# --- Constants ---
NODE_RADIUS = 20
NODE_OUTLINE_WIDTH = 2
EDGE_WIDTH = 2
NODE_COLOR_DEFAULT = "lightblue"
NODE_COLOR_VISITING = "yellow"
NODE_COLOR_VISITED = "deepskyblue"
NODE_COLOR_START = "lightgreen"
TEXT_COLOR = "black"
HIGHLIGHT_COLOR = "lightcoral"
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
CODE_WIDTH = 50
CODE_HEIGHT = 20
DELAY_MS = 700 # Delay between visualization steps in milliseconds

# --- Graph Data (Fixed) ---
graph = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['A', 'H'],
    'E': ['B'],
    'F': ['C'],
    'G': ['C', 'I'],
    'H': ['D'],
    'I': ['G']
}

# --- Node Positions (Fixed for layout) ---
node_positions = {
    'A': (CANVAS_WIDTH // 2, 50),
    'B': (CANVAS_WIDTH // 4, 150),
    'C': (CANVAS_WIDTH // 2, 150),
    'D': (3 * CANVAS_WIDTH // 4, 150),
    'E': (CANVAS_WIDTH // 4, 250),
    'F': (CANVAS_WIDTH // 2 - 50, 250),
    'G': (CANVAS_WIDTH // 2 + 50, 250),
    'H': (3 * CANVAS_WIDTH // 4, 250),
    'I': (CANVAS_WIDTH // 2 + 50, 350)
}

# --- Pseudo Code ---
DFS_CODE = [
    "DFS(graph, start_node):",
    "  visited = set()",
    "  stack = [start_node]",
    "  while stack:",
    "    node = stack.pop()",
    "    if node not in visited:",
    "      mark node as visiting", # Visualization Step
    "      visited.add(node)",
    "      mark node as visited",  # Visualization Step
    "      for neighbor in reversed(graph[node]):", # Reverse for visual order
    "        if neighbor not in visited:",
    "          stack.append(neighbor)",
    "          mark edge to neighbor", # Visualization Step
]

BFS_CODE = [
    "BFS(graph, start_node):",
    "  visited = set()",
    "  queue = deque([start_node])",
    "  visited.add(start_node)",
    "  mark start_node as visiting", # Visualization Step
    "  while queue:",
    "    node = queue.popleft()",
    "    mark node as visited",    # Visualization Step
    "    for neighbor in graph[node]:",
    "      if neighbor not in visited:",
    "        visited.add(neighbor)",
    "        queue.append(neighbor)",
    "        mark neighbor as visiting", # Visualization Step
    "        mark edge to neighbor",   # Visualization Step
]

# --- Main Application Class ---
class GraphVisualizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Traversal Visualizer (DFS/BFS)")
        self.master.geometry("1000x650") # Adjusted window size

        # --- Styling ---
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", font=('Helvetica', 10))
        style.configure("TLabel", padding=5, font=('Helvetica', 11))
        style.configure("TCombobox", padding=5, font=('Helvetica', 10))

        # --- Data Structures ---
        self.node_objects = {}  # Stores canvas oval IDs for nodes
        self.text_objects = {}  # Stores canvas text IDs for node labels
        self.edge_objects = {}  # Stores canvas line IDs for edges ((u, v): line_id)

        # --- Control Variables ---
        self.selected_algorithm = tk.StringVar(value="DFS")
        self.start_node = tk.StringVar(value=list(graph.keys())[0]) # Default start node
        self.is_running = False # Flag to prevent concurrent runs

        # --- GUI Layout ---
        # Main frame
        main_frame = ttk.Frame(master, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Left frame for controls and code
        left_frame = ttk.Frame(main_frame, width=350)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False) # Prevent resizing based on content

        # Right frame for canvas
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # --- Controls ---
        controls_frame = ttk.LabelFrame(left_frame, text="Controls", padding="10")
        controls_frame.pack(pady=10, padx=5, fill=tk.X)

        ttk.Label(controls_frame, text="Algorithm:").grid(row=0, column=0, sticky=tk.W, pady=2)
        algo_combo = ttk.Combobox(controls_frame, textvariable=self.selected_algorithm, values=["DFS", "BFS"], state="readonly", width=10)
        algo_combo.grid(row=0, column=1, sticky=tk.EW, pady=2, padx=5)
        algo_combo.bind("<<ComboboxSelected>>", self.update_code_display)

        ttk.Label(controls_frame, text="Start Node:").grid(row=1, column=0, sticky=tk.W, pady=2)
        node_combo = ttk.Combobox(controls_frame, textvariable=self.start_node, values=list(graph.keys()), state="readonly", width=10)
        node_combo.grid(row=1, column=1, sticky=tk.EW, pady=2, padx=5)

        self.run_button = ttk.Button(controls_frame, text="Run", command=self.run_visualization)
        self.run_button.grid(row=2, column=0, pady=10, padx=5, sticky=tk.EW)

        self.reset_button = ttk.Button(controls_frame, text="Reset", command=self.reset_visualization)
        self.reset_button.grid(row=2, column=1, pady=10, padx=5, sticky=tk.EW)

        # --- Code Display ---
        code_frame = ttk.LabelFrame(left_frame, text="Pseudo Code", padding="10")
        code_frame.pack(pady=10, padx=5, fill=tk.BOTH, expand=True)

        self.code_text = tk.Text(code_frame, wrap=tk.WORD, height=CODE_HEIGHT, width=CODE_WIDTH,
                                 font=("Courier New", 10), relief=tk.SUNKEN, borderwidth=1)
        self.code_text.pack(expand=True, fill=tk.BOTH)
        self.code_text.tag_configure("highlight", background=HIGHLIGHT_COLOR)
        self.code_text.config(state=tk.DISABLED) # Read-only

        # --- Canvas ---
        self.canvas = tk.Canvas(right_frame, bg="white", width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                                relief=tk.SUNKEN, borderwidth=1)
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # --- Initial Setup ---
        self.draw_graph()
        self.update_code_display() # Load initial code

    # --- Drawing Functions ---
    def draw_graph(self):
        """Draws the initial graph on the canvas."""
        self.canvas.delete("all") # Clear previous drawings
        self.node_objects.clear()
        self.text_objects.clear()
        self.edge_objects.clear()

        # Draw edges first (so nodes are on top)
        for u, neighbors in graph.items():
            for v in neighbors:
                # Avoid drawing duplicate edges (e.g., A->B and B->A)
                # Only draw if u < v alphabetically to draw each edge once
                if u < v:
                    x1, y1 = node_positions[u]
                    x2, y2 = node_positions[v]
                    line_id = self.canvas.create_line(
                        x1, y1, x2, y2,
                        width=EDGE_WIDTH, fill="gray"
                    )
                    self.edge_objects[(u, v)] = line_id
                    self.edge_objects[(v, u)] = line_id # Store both directions for lookup

        # Draw nodes
        for node, (x, y) in node_positions.items():
            # Create node circle
            oval_id = self.canvas.create_oval(
                x - NODE_RADIUS, y - NODE_RADIUS,
                x + NODE_RADIUS, y + NODE_RADIUS,
                fill=NODE_COLOR_DEFAULT, outline="black", width=NODE_OUTLINE_WIDTH
            )
            # Create node label
            text_id = self.canvas.create_text(x, y, text=node, fill=TEXT_COLOR, font=font.Font(weight='bold'))
            self.node_objects[node] = oval_id
            self.text_objects[node] = text_id

    def update_node_color(self, node, color):
        """Updates the fill color of a specific node."""
        if node in self.node_objects:
            self.canvas.itemconfig(self.node_objects[node], fill=color)
            self.master.update() # Force GUI update

    def update_edge_color(self, u, v, color):
        """Updates the color of a specific edge."""
        edge = tuple(sorted((u, v))) # Ensure consistent key format
        if edge in self.edge_objects:
             self.canvas.itemconfig(self.edge_objects[edge], fill=color, width=EDGE_WIDTH + 1) # Make highlighted edge thicker
             self.master.update()
        elif (u, v) in self.edge_objects: # Check original direction if sorted failed (shouldn't happen with current setup)
             self.canvas.itemconfig(self.edge_objects[(u, v)], fill=color, width=EDGE_WIDTH + 1)
             self.master.update()


    # --- Code Highlighting ---
    def update_code_display(self, event=None):
        """Loads the pseudo-code for the selected algorithm."""
        self.code_text.config(state=tk.NORMAL) # Enable editing
        self.code_text.delete('1.0', tk.END)   # Clear existing text
        algo = self.selected_algorithm.get()
        code_lines = DFS_CODE if algo == "DFS" else BFS_CODE
        for i, line in enumerate(code_lines):
             # Indentation matters for line numbers in Text widget
            self.code_text.insert(tk.END, f"{line}\n")
        self.code_text.config(state=tk.DISABLED) # Disable editing
        self.current_highlighted_line = None

    def highlight_code_line(self, line_index):
        """Highlights a specific line index (0-based) in the code display."""
        if self.current_highlighted_line is not None:
            # Line numbers in Text widget are 1-based
            start = f"{self.current_highlighted_line + 1}.0"
            end = f"{self.current_highlighted_line + 1}.end"
            self.code_text.tag_remove("highlight", start, end)

        if line_index is not None:
            start = f"{line_index + 1}.0"
            end = f"{line_index + 1}.end"
            self.code_text.tag_add("highlight", start, end)
            self.code_text.see(start) # Scroll to the highlighted line
            self.current_highlighted_line = line_index
        else:
            self.current_highlighted_line = None

        self.master.update() # Force GUI update

    # --- Visualization Logic ---
    def run_visualization(self):
        """Starts the selected graph traversal visualization."""
        if self.is_running:
            print("Visualization already in progress.")
            return

        self.is_running = True
        self.run_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.reset_visualization(clear_code_highlight=False) # Reset colors but keep code

        start_node_val = self.start_node.get()
        algo = self.selected_algorithm.get()

        try:
            if algo == "DFS":
                self.visualize_dfs(start_node_val)
            else: # BFS
                self.visualize_bfs(start_node_val)
        except Exception as e:
            print(f"An error occurred during visualization: {e}")
            self.reset_visualization() # Ensure reset even on error
        finally:
            # Use 'after' to re-enable buttons slightly after the visualization ends
            # This ensures the last step is visible before buttons are active
            self.master.after(DELAY_MS + 100, self.enable_controls)


    def enable_controls(self):
        """Re-enables control buttons and resets running flag."""
        self.is_running = False
        self.run_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.highlight_code_line(None) # Clear code highlight


    def visualize_dfs(self, start_node):
        """Performs DFS traversal with visualization steps."""
        self.highlight_code_line(0) # DFS function call
        self.master.after(DELAY_MS)

        visited = set()
        stack = [(start_node, None)] # Store (node, parent_edge) for edge highlighting

        self.highlight_code_line(1) # visited = set()
        self.master.after(DELAY_MS)
        self.highlight_code_line(2) # stack = [start_node]
        self.master.after(DELAY_MS)

        while stack:
            self.highlight_code_line(3) # while stack:
            self.master.after(DELAY_MS // 2) # Faster check

            node, parent_node = stack.pop()
            self.highlight_code_line(4) # node = stack.pop()
            self.master.after(DELAY_MS)

            self.highlight_code_line(5) # if node not in visited:
            self.master.after(DELAY_MS)
            if node not in visited:
                # Visualization: Mark as visiting
                self.highlight_code_line(6) # mark node as visiting
                self.update_node_color(node, NODE_COLOR_VISITING)
                # Highlight edge from parent if applicable
                if parent_node:
                    self.update_edge_color(parent_node, node, HIGHLIGHT_COLOR)
                self.master.after(DELAY_MS)

                visited.add(node)
                self.highlight_code_line(7) # visited.add(node)
                self.master.after(DELAY_MS)

                # Visualization: Mark as visited
                self.highlight_code_line(8) # mark node as visited
                self.update_node_color(node, NODE_COLOR_VISITED)
                self.master.after(DELAY_MS)

                # Add neighbors to stack (reversed for intuitive order)
                self.highlight_code_line(9) # for neighbor in reversed(graph[node]):
                self.master.after(DELAY_MS // 2)
                neighbors = reversed(graph.get(node, [])) # Use get for safety
                for neighbor in neighbors:
                    self.highlight_code_line(10) # if neighbor not in visited:
                    self.master.after(DELAY_MS // 2)
                    if neighbor not in visited:
                        self.highlight_code_line(11) # stack.append(neighbor)
                        stack.append((neighbor, node)) # Add neighbor and its parent
                        self.master.after(DELAY_MS)
                        # Visualization: Indicate edge consideration (optional, can be noisy)
                        # self.highlight_code_line(12) # mark edge to neighbor
                        # self.update_edge_color(node, neighbor, "orange")
                        # self.master.after(DELAY_MS // 2)
                    else:
                         # Optional: Briefly show check on already visited neighbor
                         self.update_node_color(neighbor, "lightgrey")
                         self.master.after(DELAY_MS // 4)
                         self.update_node_color(neighbor, NODE_COLOR_VISITED) # Revert color
                         self.master.after(DELAY_MS // 4)
            else:
                 # Optional: Briefly show check on already visited node from stack
                 self.update_node_color(node, "lightgrey")
                 self.master.after(DELAY_MS // 4)
                 if node in visited: # Ensure it was actually visited before changing back
                     self.update_node_color(node, NODE_COLOR_VISITED)
                 else: # Should not happen in standard DFS, but for safety
                     self.update_node_color(node, NODE_COLOR_DEFAULT)
                 self.master.after(DELAY_MS // 4)


        self.highlight_code_line(None) # End of visualization


    def visualize_bfs(self, start_node):
        """Performs BFS traversal with visualization steps."""
        self.highlight_code_line(0) # BFS function call
        self.master.after(DELAY_MS)

        visited = set()
        queue = deque([(start_node, None)]) # Store (node, parent_node) for edge highlighting

        self.highlight_code_line(1) # visited = set()
        self.master.after(DELAY_MS)

        self.highlight_code_line(2) # queue = deque([start_node])
        visited.add(start_node)
        self.highlight_code_line(3) # visited.add(start_node)
        self.master.after(DELAY_MS)

        # Visualization: Mark start node as visiting
        self.highlight_code_line(4) # mark start_node as visiting
        self.update_node_color(start_node, NODE_COLOR_VISITING)
        self.master.after(DELAY_MS)

        while queue:
            self.highlight_code_line(5) # while queue:
            self.master.after(DELAY_MS // 2) # Faster check

            node, parent_node = queue.popleft()
            self.highlight_code_line(6) # node = queue.popleft()
            self.master.after(DELAY_MS)

            # Visualization: Mark node as visited
            self.highlight_code_line(7) # mark node as visited
            self.update_node_color(node, NODE_COLOR_VISITED)
            # Highlight edge from parent if applicable
            if parent_node:
                self.update_edge_color(parent_node, node, HIGHLIGHT_COLOR)
            self.master.after(DELAY_MS)

            self.highlight_code_line(8) # for neighbor in graph[node]:
            self.master.after(DELAY_MS // 2)
            neighbors = graph.get(node, []) # Use get for safety
            for neighbor in neighbors:
                self.highlight_code_line(9) # if neighbor not in visited:
                self.master.after(DELAY_MS // 2)
                if neighbor not in visited:
                    visited.add(neighbor)
                    self.highlight_code_line(10) # visited.add(neighbor)
                    self.master.after(DELAY_MS)

                    queue.append((neighbor, node)) # Add neighbor and its parent
                    self.highlight_code_line(11) # queue.append(neighbor)
                    self.master.after(DELAY_MS)

                    # Visualization: Mark neighbor as visiting (about to be processed)
                    self.highlight_code_line(12) # mark neighbor as visiting
                    self.update_node_color(neighbor, NODE_COLOR_VISITING)
                    self.master.after(DELAY_MS)

                    # Visualization: Highlight edge being added
                    self.highlight_code_line(13) # mark edge to neighbor
                    self.update_edge_color(node, neighbor, HIGHLIGHT_COLOR) # Highlight edge earlier for BFS
                    self.master.after(DELAY_MS)
                else:
                    # Optional: Briefly show check on already visited neighbor
                    if neighbor in self.node_objects: # Check if neighbor exists visually
                        current_color = self.canvas.itemcget(self.node_objects[neighbor], "fill")
                        if current_color != NODE_COLOR_VISITING and current_color != NODE_COLOR_VISITED:
                            # Only flash if not already highlighted
                            self.update_node_color(neighbor, "lightgrey")
                            self.master.after(DELAY_MS // 4)
                            self.update_node_color(neighbor, current_color) # Revert color
                            self.master.after(DELAY_MS // 4)


        self.highlight_code_line(None) # End of visualization


    def reset_visualization(self, clear_code_highlight=True):
        """Resets the graph colors and clears highlights."""
        if self.is_running: # Prevent reset during active run
            return

        # Reset node colors
        for node, oval_id in self.node_objects.items():
            self.canvas.itemconfig(oval_id, fill=NODE_COLOR_DEFAULT)

        # Reset edge colors
        for edge, line_id in self.edge_objects.items():
             # Check if the item still exists before configuring
            if line_id in self.canvas.find_all():
                self.canvas.itemconfig(line_id, fill="gray", width=EDGE_WIDTH)

        # Clear code highlight
        if clear_code_highlight:
            self.highlight_code_line(None)

        self.master.update()


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualizerApp(root)
    root.mainloop()
