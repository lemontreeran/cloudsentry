from arango import ArangoClient
from langchain_community.graphs.arangodb_graph import ArangoGraph
from config.settings import ARANGO_ENDPOINT, ARANGO_DATABASE, ARANGO_USERNAME, ARANGO_PASSWORD

# Connect to ArangoDB
client = ArangoClient(hosts=ARANGO_ENDPOINT)
db = client.db(ARANGO_DATABASE, username=ARANGO_USERNAME, password=ARANGO_PASSWORD)

# Initialize LangChain ArangoGraph Wrapper
arango_graph = ArangoGraph(db)
