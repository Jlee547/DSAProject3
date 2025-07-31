import heapq

def dijkstra(src: int, dst: int, graph: dict[int, set[tuple[int,float]]]) -> list[str]:
    nodes = []

    for node in graph.keys():
        nodes.append(node)

    
    #Start and destination nodes
    startNode = src
    destinationNode = dst

    #Distances and visited nodes
    distances = {}
    visited = set()

    #Path from start to destination
    path = []

    previousNode = {}

    #Initializes distances and previous nodes
    for node in nodes:
        distances[node] = float('inf')
        previousNode[node] = None

    #Creates a min heap for the start node 
    minHeap = []
    heapq.heaqpush(minHeap, (startNode, 0))
    distances[startNode] = 0

    #Dijkstra's algorithm
    while True:
        currentNode, currentDistance = heapq.heappop(minHeap)

        if currentNode is None or currentNode == destinationNode:
            break

        visited.add(currentNode)

        #Looks at the neighbors of the currentNodes and checks if the distance is less than the current distance if it is it does dijkstra's logic
        for neighbor, length in graph[currentNode]:
            if neighbor not in visited:
                altDistance = distances[currentNode] + length
                if altDistance < distances[neighbor]:
                    distances[neighbor] = altDistance
                    previousNode[neighbor] = currentNode
                    heapq.heaqpush(minHeap, (neighbor, altDistance))

    currentNode = destinationNode

    #Gets the path from the destinationNode to the startNode
    while currentNode is not None:
        path.append(currentNode)
        currentNode = previousNode[currentNode]
    
    #Reverses the path cause it was from destinationNode to startNode now its startNode to destinationNode
    path.reverse()

    return path