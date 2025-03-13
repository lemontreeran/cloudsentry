import json

# Load the exported Neo4j JSON
with open("neo4j_export.json", "r") as f:
    data = json.load(f)

# Save nodes
with open("nodes.json", "w") as f:
    json.dump(data["nodes"], f, indent=4)

# Save edges
with open("edges.json", "w") as f:
    json.dump(data["edges"], f, indent=4)

print("✅ Split JSON into nodes.json and edges.json")
