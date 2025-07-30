
'''
takes in 1 string source id, 1 string destination id
returns the shortest path between the 2 nodes in the form of a list of nodes.

'''
import json


def dijkstra(src: str, dst: str) -> list[str]:
    
    with open("project3_nodes.json", "r") as f:
        nodes = json.load(f)
    
    with open("project3_edges.json", "r") as f:
        edges = json.load(f)

    #Making an adjacency list
    adjacencyList = {}
    for edge in edges:
        start, destination, length = edge["u"], edge["v"], edge["length"]
        if start not in adjacencyList:
            adjacencyList[start] = []
        adjacencyList[start].append((destination, length))
    
    # Dijkstra's algorithm
    startNode = src
    destinationNode = dst

    distances = {}
    visited = {}

    path = []
    previousNode = {}

    #Created the intial distances and visited nodes
    for node in nodes:
        distances[node] = float('inf')
        visited[node] = False
        previousNode[node] = None


    distances[startNode] = 0
    
    
    while True:
        minDistance = float('inf')
        currentNode = None

        #Gets the node with the least distance 
        for node in nodes:
            if not visited[node] and distances[node] < minDistance:
                minDistance = distances[node]
                currentNode = node
        
        if currentNode is None or currentNode == destinationNode:
            break

        visited[currentNode] = True

        #Just double checks that all nodes are in the list so it prevents any errors
        for node in nodes:
            if node not in adjacencyList:
                adjacencyList[node] = []
        
        #Looks at the neighbors of the currentNodes and checks if the distance is less than the current distance
        for neighbor, length in adjacencyList[currentNode]:
            if not visited[neighbor]:
                altDistance = distances[currentNode] + length
                if altDistance < distances[neighbor]:
                    distances[neighbor] = altDistance
                    previousNode[neighbor] = currentNode


    currentNode = destinationNode

    #Gets the path from the destinationNode to the startNode
    while currentNode is not None:
        path.append(currentNode)
        currentNode = previousNode[currentNode]

    #Reverses the path so now its from startNode to destinationNode
    path.reverse()

    return path
