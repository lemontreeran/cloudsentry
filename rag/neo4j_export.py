from neo4j import GraphDatabase
import json
from datetime import datetime
from neo4j.time import DateTime as Neo4jDateTime  # Import Neo4j's DateTime

# Neo4j Connection Details
NEO4J_URI = "bolt://localhost:7687"  # Change if needed
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Function to convert Neo4j DateTime objects into JSON serializable formats
def serialize_value(value):
    if isinstance(value, Neo4jDateTime):  # Convert Neo4j DateTime to string
        return value.to_native().isoformat()
    elif isinstance(value, datetime):  # Convert Python datetime
        return value.isoformat()
    elif isinstance(value, list):  # Convert lists recursively
        return [serialize_value(v) for v in value]
    elif isinstance(value, dict):  # Convert dictionary recursively
        return {k: serialize_value(v) for k, v in value.items()}
    return value  # Keep other values as-is

# Fetch nodes (without APOC)
def fetch_nodes(tx):
    result = tx.run("""
        MATCH (n) 
        RETURN id(n) AS id, labels(n) AS labels, properties(n) AS properties
    """)
    nodes = []
    for record in result:
        node = {
            "_key": str(record["id"]),
            "labels": record["labels"],
            **serialize_value(record["properties"])  # Convert properties
        }
        nodes.append(node)
    return nodes

# Fetch relationships (without APOC)
def fetch_relationships(tx):
    result = tx.run("""
        MATCH (a)-[r]->(b) 
        RETURN id(a) AS source, id(b) AS target, type(r) AS type, properties(r) AS properties
    """)
    relationships = []
    for record in result:
        relationship = {
            "_from": f"nodes/{record['source']}",
            "_to": f"nodes/{record['target']}",
            "type": record["type"],
            **serialize_value(record["properties"])  # Convert properties
        }
        relationships.append(relationship)
    return relationships

# Extract and Save Data
with driver.session() as session:
    nodes = session.read_transaction(fetch_nodes)
    relationships = session.read_transaction(fetch_relationships)

    # Structure for JSON export
    neo4j_data = {
        "nodes": nodes,
        "edges": relationships
    }

    # Save as JSON file
    with open("neo4j_export.json", "w") as f:
        json.dump(neo4j_data, f, indent=4)

print("✅ Exported data from Neo4j to neo4j_export.json")
driver.close()
