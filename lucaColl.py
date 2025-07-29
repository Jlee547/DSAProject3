
'''
takes in 1 string source id, 1 string destination id
returns the shortest path between the 2 nodes in the form of a list of nodes.
'''
import json
import heapq # priority queue (built-in module)
import math

def astar(src: str, dst: str) -> list[str]:
    with open("project3_nodes.json", "r") as f:
        nodes = json.load(f)
    
    with open("project3_edges.json", "r") as f:
        edges = json.load(f)
    
    # build graph (adjaceny list) w/ edges 
    g = {} 
    for edge in edges:
        u = edge["u"] # start
        v = edge["v"] # end
        len = edge["length"] # length
        # both directions 
        if u not in g:
            g[u] = {}
        g[u][v] = len
        if v not in g:
            v[u] = {}
        g[v][u] = len
    # check source or destination node 
    if src not in g or dst not in g:
        return []
    # priority queue 
    open_nodes = []
    heapq.heappush(open_nodes, (0,src))
    # track path 
