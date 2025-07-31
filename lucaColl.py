
'''
takes in 1 string source id, 1 string destination id
returns the shortest path between the 2 nodes in the form of a list of nodes.
'''
import heapq

def astar(src: int, dst: int, graph: dict[int, set[tuple[int, float]]]) -> list[str]:
    if src not in graph or dst not in graph:
        return []
    # priority queue 
    exp_nodes = []
    heapq.heappush(exp_nodes, (0, src))
    # tracking 
    origin = {}
    cost = {}
    est_cost = {}
    # costs 
    for node in graph:
        cost[node] = float('inf')
        est_cost[node] = float('inf')
    
    cost[src] = 0
    est_cost[src] = 0
    # search 
    while exp_nodes:
        curr_est, curr_node = heapq.heappop(exp_nodes)
        # path 
        if curr_node == dst:
            path = []
            while curr_node in origin:
                path.append(str(curr_node))
                curr_node = origin[curr_node]
            path.append(str(src))
            path.reverse()
            return path
        if curr_est > est_cost[curr_node]:
            continue
        # neighbors 
        for near, dist in graph[curr_node]:
            new_cost = cost[curr_node] + dist
            if new_cost < cost[near]:
                origin[near] = curr_node
                cost[near] = new_cost
                est_cost[near] = new_cost
                heapq.heappush(exp_nodes, (est_cost[near], near))
    
    return []