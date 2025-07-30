
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
        length = edge["length"] # length
        # both directions 
        if u not in g:
            g[u] = {}
        g[u][v] = length
        if v not in g:
            g[v] = {}
        g[v][u] = length
    # check source or destination node 
    if src not in g or dst not in g:
        return []
    # priority queue 
    exp_nodes = []
    heapq.heappush(exp_nodes, (0,src))
    # track path 
    origin = {}
    # https://stackoverflow.com/questions/42884863/a-star-algorithm-understanding-the-f-g-h-scores
    # cost from start to current node (g score)
    cost = {}
    for node in g:
        cost[node] = float('inf')
    cost[src] = 0
    # estimated cost (f score)
    est_cost = {}
    for node in g:
        est_cost[node] = float('inf')
    est_cost[src] = 0 # heuristic value for start node 
    # nodes to explore 
    exp_nodes = []
    heapq.heappush(exp_nodes, (0, src))
    # destination coordinates 
    dst_node = nodes[dst]
    dst_lt = dst_node["lat"]
    dst_ln = dst_node["lon"]
    # search 
    while exp_nodes:
        curr_est, curr_node = heapq.heappop(exp_nodes)
        if curr_node == dst:
            path = []
            while curr_node in origin:
                path.append(curr_node)
                curr_node = origin[curr_node]
            path.append(src)
            path.reverse()
            return path 
        # skip if better path found 
        if curr_est > est_cost[curr_node]:
            continue
        # check nearby nodes 
        for near, dist in g[curr_node].items():
            new_cost = cost[curr_node] + dist
            if new_cost < cost[near]:
                origin[near] = curr_node
                cost[near] = new_cost
                # heuristic calculation 
                near_node = nodes[near]
                near_lt = near_node["lat"]
                near_ln = near_node["lon"]
                dif_lt = dst_lt - near_lt
                dif_ln = dst_ln - near_ln
                heur = math.sqrt(dif_lt*dif_lt + dif_ln*dif_ln)
                est_cost[near] = heur + new_cost
                heapq.heappush(exp_nodes, (est_cost[near], near))
        
    return []
    