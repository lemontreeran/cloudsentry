from arango import ArangoClient

# Connect to ArangoDB
client = ArangoClient()
db = client.db("cloudsentry", username="root", password="password")

# Create Graph (if not exists)
graph_name = "cloud_attack_graph"
if not db.has_graph(graph_name):
    graph = db.create_graph(graph_name)
    
    # Define nodes and edges collections
    if not db.has_collection("nodes"):
        db.create_collection("nodes")
    if not db.has_collection("edges"):
        db.create_collection("edges", edge=True)
    
    # Add edge definitions (relationship mappings)
    graph.create_edge_definition(
        edge_collection="edges",
        from_vertex_collections=["nodes"],
        to_vertex_collections=["nodes"]
    )

print("✅ Cloud Attack Graph Created Successfully!")
