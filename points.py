import osmnx as ox
import json
from osmnx.distance import add_edge_lengths


# Define counties
places = [
    "Alachua County, Florida, USA",
    "Baker County, Florida, USA",
    "Bradford County, Florida, USA",
    "Clay County, Florida, USA",
    "Columbia County, Florida, USA",
    "Duval County, Florida, USA",
    "Gilchrist County, Florida, USA",
    "Hamilton County, Florida, USA",
    "Madison County, Florida, USA",
    "Nassau County, Florida, USA",
    "Putnam County, Florida, USA",
    "St. Johns County, Florida, USA",
    "Suwannee County, Florida, USA",
    "Union County, Florida, USA"
]

# Download road network
G = ox.graph_from_place(places, network_type='drive')
G = add_edge_lengths(G)

# Extract minimal node info (for A*)
nodes = {
    str(n): {
        "lat": float(data["y"]),
        "lon": float(data["x"])
    } for n, data in G.nodes(data=True)
}

# Extract minimal edge info (for both algorithms)
#u is the starting node, v is the ending node
edges = []
for u, v, data in G.edges(data=True):
    edges.append({
        "u": str(u),
        "v": str(v),
        "length": float(data.get("length", 1.0))  # fallback if length missing
    })

# Save to JSON files
with open("project3_nodes.json", "w") as f:
    json.dump(nodes, f, indent=2)

with open("project3_edges.json", "w") as f:
    json.dump(edges, f, indent=2)

print(f"Saved {len(nodes)} nodes and {len(edges)} edges")
