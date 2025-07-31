
'''
takes in 1 string source id, 1 string destination id
returns the shortest path between the 2 nodes in the form of a list of nodes.

'''

import heapq

def dijkstra(src: int, dst: int, graph: dict[int, set[tuple[int, float]]]) -> list[str]:
    
    nodes = []

    for node in graph.keys():
        nodes.append(node)

    
    # Dijkstra's algorithm
    startNode = src
    destinationNode = dst

    distances = {}
    visited = set()

    path = []
    previousNode = {}

    #Created the intial distances and visited nodes
    for node in nodes:
        distances[node] = float('inf')
        previousNode[node] = None

    minHeap = []
    heapq.heappush(minHeap, (startNode, 0))
    distances[startNode] = 0
    
    
    while True:
        currentNode, currentDistance = heapq.heappop(minHeap)
        
        if currentNode is None or currentNode == destinationNode:
            break

        visited.add(currentNode)

        
        #Looks at the neighbors of the currentNodes and checks if the distance is less than the current distance
        for neighbor, length in graph[currentNode]:
            if neighbor not in visited:
                altDistance = distances[currentNode] + length
                if altDistance < distances[neighbor]:
                    distances[neighbor] = altDistance
                    previousNode[neighbor] = currentNode
                    heapq.heappush(minHeap, (neighbor, altDistance))


    currentNode = destinationNode

    #Gets the path from the destinationNode to the startNode
    while currentNode is not None:
        path.append(currentNode)
        currentNode = previousNode[currentNode]

    #Reverses the path so now its from startNode to destinationNode
    path.reverse()

    return path
