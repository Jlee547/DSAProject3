import json
from collections import defaultdict, deque
import time
import random
import math



class GraphGenerator:

    class Node:
        def __init__(self, id=0, lat=0.00, lon=0.00, x=0.00, y=0.00):
            self.id = id
            self.lat = lat
            self.lon = lon
            self.x = x
            self.y = y


    def __init__(self, node_count):

        '''
        graph[85929358923] = set((4289124, 2352), (123491234, 325), (2352346235,))
        
        '''
        self.node_count = node_count
        self.graph = defaultdict(set)   # All nodes with a value of a set of tuples where tuple[0] is the neighbor node and tuple[1] is the weight
        self.nodes = dict()             # Dictionary storing the key as the int (id) and a value of the node object
        self.node_set = set()           # Int (id) value for all considered nodes
        self.graph_subset = defaultdict(set) #subset graph

        self.generate_graph()
        self.sample_connected_subgraph(node_count)
        self.generate_nodes()
        self.generate_subset_graph()
    

    def generate_graph(self):
        # creates graph from entire dataset
        start = time.time()
        with open("project3_edges.json", "r") as f:
            edges = json.load(f)

            for edge in edges:
                u = int(edge["u"])
                v = int(edge["v"])
                weight = float(edge["length"])

                self.graph[u].add((v, weight))
                self.graph[v].add((u, weight))
        end = time.time()
        print(f"It took {end - start} time to build the graph")


    def generate_nodes(self):
        #creates node dictionary that assigns a node object to an id
        start = time.time()
        with open("project3_nodes.json", "r") as f:
            nodes_f = json.load(f)

            
            for node in nodes_f:
                if int(node) in self.node_set:
                    lat = float(nodes_f[node]["lat"])
                    lon = float(nodes_f[node]["lon"])
                    self.nodes[int(node)] = GraphGenerator.Node(id=int(node), lat=lat, lon=lon)

        end = time.time()
        print(f"It took {end - start} time to build the nodes")

    
    def sample_connected_subgraph(self, n):
        # picks random seed and continues to search throughout the entire graph
        remaining = set(self.graph.keys())
        while remaining:

            seed = random.choice(tuple(remaining))
            visited = {seed}
            q = deque([seed])

            #performs a bfs and will return if graph has enough nodes, otherwise, continue searching original graph for a large enoughsubset
            while q and len(visited) < n:
                u = q.popleft()
                for v, _ in self.graph[u]:
                    if v not in visited:
                        visited.add(v)
                        q.append(v)
                        if len(visited) >= n:
                            break

            if len(visited) >= n:
                print(f"Found connected component of size {len(visited)}")
                self.node_set = visited
                return

            remaining -= visited


        print(f"No connected component of size ≥ {n} exists in the graph.")
        self.node_set = set()

    def generate_subset_graph(self):
        #for every node,
        for node in self.node_set:
            # consider neighbors
            for v, weight in self.graph[node]:
                #consider if neighbor is in graph subset, if so, add to subset graph
                if v in self.node_set:
                    real_weight = math.sqrt((self.nodes[node].x - self.nodes[v].x) ** 2 + (self.nodes[node].y - self.nodes[v].y) ** 2)
                    self.graph_subset[node].add((v, real_weight))
                    self.graph_subset[v].add((node, real_weight))
    
    def draw_to_canvas(self, canvas):
        W = int(canvas['width'])
        H = int(canvas['height'])

        # list of lats and lons
        lats = [self.nodes[n].lat for n in self.nodes]
        lons = [self.nodes[n].lon for n in self.nodes]
        lat_min, lat_max = min(lats), max(lats)
        lon_min, lon_max = min(lons), max(lons)

        # iterate through all nodes and draw based on percent of range of lats and lons, then set node position
        for node in self.nodes:
            x = (self.nodes[node].lon - lon_min)/(lon_max - lon_min) * 900
            y = (lat_max - self.nodes[node].lat)/(lat_max - lat_min) * 700
            canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")
            self.nodes[node].x = x
            self.nodes[node].y = y
    
    def draw_edges(self, canvas):
        # Every considered node id
        seen = set()
        for node in self.node_set:
            
            # Search for edge tuples in set, making sure to check for reversed direction
            for v, weight in self.graph[node]:
                if v in self.node_set and (v, node) not in seen:
                    canvas.create_line(self.nodes[node].x, self.nodes[node].y, self.nodes[v].x, self.nodes[v].y, fill="black", width=1) # create line from origin(node) to neighbor(v)
                    seen.add((node, v))

    def reset_graph(self, new_node_count):
        self.node_count = new_node_count

        self.nodes.clear()
        self.node_set.clear()
        self.graph_subset.clear()

        self.sample_connected_subgraph(self.node_count)
        self.generate_nodes()
        self.generate_subset_graph()

#generator = GraphGenerator(1000)

''' random - 
            random_edges = random.sample(edges, node_count)
            for edge in random_edges:
                u = int(edge["u"])
                v = int(edge["v"])
                weight = float(edge["length"])

                self.graph[u].add((v, weight))
                self.graph[v].add((u, weight))
'''



'''
def search_1():
    print("Search_1")

def search_2():
    print("Search_2")

def on_canvas_click(event):
    x, y = event.x, event.y
    canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")

root = tk.Tk()
root.geometry("900x800")
root.resizable(False, False)
root.title("Pathfinding")

top_frame = tk.Frame(root)
top_frame.pack(side="top")

button1 = tk.Button(top_frame, text="A*", command=search_1)
button2 = tk.Button(top_frame, text="Dijkstras*", command=search_2)
button1.pack(side="left", padx=5, pady=5)
button2.pack(side="left", padx=5, pady=5)


canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)
canvas.bind("<Button-1>", on_canvas_click)

root.mainloop()'''