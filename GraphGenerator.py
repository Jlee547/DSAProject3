import json
from collections import defaultdict, deque
import time
import random




class GraphGenerator:

    class Node:
        def __init__(self, id=0, lat=0.00, lon=0.00, x=0.00, y=0.00):
            self.id = id
            self.lat = lat
            self.lon = lon
            self.x = x
            self.y = y


    def __init__(self, node_count):
        self.graph = defaultdict(set)   # All nodes with a value of a set of tuples where tuple[0] is the neighbor node and tuple[1] is the weight
        self.nodes = dict()             # Dictionary storing the key as the int (id) and a value of the node object
        self.node_set = set()           # Int (id) value for all considered nodes

        self.generate_graph()
        self.sample_connected_subgraph(node_count)
        self.generate_nodes()
    

    def generate_graph(self):
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

        remaining = set(self.graph.keys())
        while remaining:

            seed = random.choice(tuple(remaining))
            visited = {seed}
            q = deque([seed])


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
    
    def draw_to_canvas(self, canvas):
        W = int(canvas['width'])
        H = int(canvas['height'])

        lats = [self.nodes[n].lat for n in self.nodes]
        lons = [self.nodes[n].lon for n in self.nodes]
        lat_min, lat_max = min(lats), max(lats)
        lon_min, lon_max = min(lons), max(lons)

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
            
            # Search for edge tuples in set
            for v, weight in self.graph[node]:
                if v in self.node_set and (v, node) not in seen:
                    canvas.create_line(self.nodes[node].x, self.nodes[node].y, self.nodes[v].x, self.nodes[v].y, fill="black", width=1) # create line from origin(node) to neighbor(v)
                    seen.add((node, v))

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