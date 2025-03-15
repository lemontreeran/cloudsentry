import json
from arango import ArangoClient
from config.settings import ARANGO_ENDPOINT, ARANGO_DATABASE, ARANGO_USERNAME, ARANGO_PASSWORD

# Connect to ArangoDB
client = ArangoClient(hosts=ARANGO_ENDPOINT)
db = client.db(ARANGO_DATABASE, username=ARANGO_USERNAME, password=ARANGO_PASSWORD)

# Load AI-inferred attack paths
with open("classified_attacks.json", "r") as f:
    attack_edges = json.load(f)

# Insert edges into ArangoDB
edge_collection = db.collection("edges")
for edge in attack_edges:
    edge_collection.insert({
        "_from": f"nodes/{edge['from']}",
        "_to": f"nodes/{edge['to']}",
        "relationship": edge["relationship"],
        "attack_vector": edge["attack_vector"]
    })

print("✅ AI-inferred attack paths imported into ArangoDB")