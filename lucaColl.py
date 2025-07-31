
'''
takes in 1 string source id, 1 string destination id
returns the shortest path between the 2 nodes in the form of a list of nodes.
'''
import heapq

def astar(src: int, dst: int, graph: dict[int, set[tuple[int, float]]]) -> list[int]:
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
                path.append(curr_node)
                curr_node = origin[curr_node]
            path.append(src)
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

# # Test cases
# if __name__ == "__main__":
#     # Test graph
#     test_graph = {
#         1: {(2, 1.5), (3, 2.0)},
#         2: {(1, 1.5), (4, 1.2)},
#         3: {(1, 2.0), (4, 1.8), (5, 2.5)},
#         4: {(2, 1.2), (3, 1.8), (5, 1.0)},
#         5: {(3, 2.5), (4, 1.0)}
#     }

#     print("Running tests...\n")

#     # Test 1: Normal path
#     result = astar(1, 5, test_graph)
#     print(f"Test 1 - Path from 1 to 5: {result}")
#     print("✓ Should be ['1','2','4','5'] or ['1','3','4','5']\n")

#     # Test 2: Same start and end
#     result = astar(3, 3, test_graph)
#     print(f"Test 2 - Path from 3 to 3: {result}")
#     print("✓ Should be ['3']\n")

#     # Test 3: No path exists
#     no_path_graph = {1: {(2, 1.0)}, 2: {(1, 1.0)}, 3: set()}
#     result = astar(1, 3, no_path_graph)
#     print(f"Test 3 - Path from 1 to 3 (no path): {result}")
#     print("✓ Should be []\n")

#     # Test 4: Direct connection
#     result = astar(2, 4, test_graph)
#     print(f"Test 4 - Path from 2 to 4: {result}")
#     print("✓ Should be ['2','4']\n")

#     # Test 5: Non-existent node
#     result = astar(1, 99, test_graph)
#     print(f"Test 5 - Path from 1 to 99: {result}")
#     print("✓ Should be []\n")

#     print("Testing complete.")