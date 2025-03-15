from langchain.tools import tool
from modules.arango_connector import arango_graph
from modules.llm_handler import llm

@tool
def text_to_aql_to_text(query: str):
    """Find attack paths dynamically from ArangoDB"""

    aql_query = """
    FOR attack IN edges
        FILTER attack.attack_vector != NULL
        RETURN {
            attack_path: CONCAT(attack._from, " → ", attack._to),
            relationship: attack.relationship,
            risk_type: attack.attack_vector
        }
    """

    attack_paths = arango_graph.db.aql.execute(aql_query)
    attack_list = list(attack_paths)

    if not attack_list:
        return "✅ No security vulnerabilities detected."

    attack_description = "\n".join([
        f"Resource: {attack['attack_path']}, Relationship: {attack['relationship']}, Risk: {attack['risk_type']}"
        for attack in attack_list
    ])

    return attack_description