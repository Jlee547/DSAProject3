import json
from collections import defaultdict, deque
import time
import random




class GraphGenerator:
    def __init__(self, node_count):
        self.graph = defaultdict(set)
        self.nodes = dict()
        self.node_set = set()

        self.generate_graph()
        self.sample_connected_subgraph(node_count)
        self.generate_nodes()

        print("Components: ", self.count_components())
    

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
                    self.nodes[int(node)] = (lat, lon)

        end = time.time()
        print(f"It took {end - start} time to build the nodes")

    def count_components(self):
        visited = set()
        components = 0

        for node in self.nodes:
            if node in visited:
                continue

            components += 1

            stack = [node]
            visited.add(node)
            while stack:
                u = stack.pop()
                for v, _ in self.graph[u]:
                    if v not in visited:
                        visited.add(v)
                        stack.append(v)

        return components
    
    def sample_connected_subgraph(self, n):
        seed = random.choice(list(self.graph.keys()))
        visited = {seed}
        q = deque([seed])

        while q and len(visited) < n:
            u = q.popleft()
            for v in self.graph[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)
                    if len(visited) >= n:
                        break
        
        self.node_set = visited

    

generator = GraphGenerator(10000)

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