
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

    #Making Dijkstra's algorithm work

    
    return []