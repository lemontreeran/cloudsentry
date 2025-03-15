import json
import os
import re
from langchain_openai import ChatOpenAI

# Load extracted Neo4j relationships
with open("neo4j_relationships.json", "r") as f:
    relationships = json.load(f)

# Ensure API Key is set
if "OPENAI_API_KEY" not in os.environ:
    print("❌ Error: OPENAI_API_KEY is not set. Please set it and try again.")
    exit(1)

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

# LLM prompt to analyze attack paths
llm_prompt = f"""
You are a cloud security expert analyzing AWS IAM relationships.
Below is a list of relationships extracted from AWS resources in Neo4j.

Analyze these relationships and classify them into security risks:
- Privilege Escalation (e.g., IAM PassRole, AssumeRole)
- Credential Theft (e.g., GetAccessKey, EC2 Metadata exposure)
- Data Exfiltration (e.g., S3 Bucket permissions)
- Service Exploits (e.g., Lambda, EC2 SSRF)

Format output as JSON: 
[{{
    "from": "IAMUser1",
    "to": "IAMRole1",
    "relationship": "iam_pass_role",
    "attack_vector": "Privilege Escalation"
}}]

Data:
{json.dumps(relationships, indent=4)}

Return only the JSON array with classified attack paths.
"""

try:
    response = llm.invoke(llm_prompt)

    # Debug: Print Raw Response
    print("🔹 Raw LLM Response:")
    print(response)

    # Check if response is empty
    if not response or not response.content:
        print("❌ Error: Empty response from LLM.")
        exit(1)

    # Remove ```json or ``` wrapping the response
    cleaned_response = re.sub(r"^```json\n|```$", "", response.content.strip(), flags=re.MULTILINE).strip()

    # Debug: Print Cleaned Response
    print("🔹 Cleaned JSON Response:", cleaned_response)

    # Parse JSON response
    classified_attacks = json.loads(cleaned_response)

    # Save results
    with open("classified_attacks.json", "w") as f:
        json.dump(classified_attacks, f, indent=4)

    print("✅ Attack paths classified and saved to classified_attacks.json")

except json.JSONDecodeError as e:
    print("❌ JSON Parsing Error:", e)
    print("🔹 Response Content:", response.content)
    exit(1)

except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    exit(1)
