# app.py
import streamlit as st
import re
from typing import Tuple, List

# Suppose these are local modules that you have in the same directory
# We'll inline their code below, but you can also import them if you prefer:
import openai

# For demonstration, we import the custom modules from local .py files:
from translate_rego_to_aws import parse_rego_policy, generate_aws_iam_policy
from verify_policy import verify_no_manager_delete

##############################################################################
# 1. LLM Utility - Mock or Real
##############################################################################

# If you have an OpenAI key, you can load it:
# openai.api_key = "YOUR_OPENAI_API_KEY"

def call_llm_for_rego_policy(requirement_text: str) -> str:
    """
    Calls an LLM (GPT-4, ChatGPT, etc.) with a prompt that includes the user's requirement.
    Returns the generated Rego policy snippet as a string.
    
    NOTE: This is a simplified example. In production, you'll handle errors,
    token limits, complex prompt engineering, etc.
    """
    # Example prompt
    prompt = f"""
You are a security policy synthesis assistant. 

Your task: Generate a Rego policy that meets this requirement:
"{requirement_text}"

Please produce a valid Rego policy snippet that:
1. Defines a rule for the 'Manager' role.
2. Allows the 'approve' action on the resource "ResourceRequests".
3. Explicitly denies the 'delete' action on "ResourceRequests" for the 'Manager' role.
4. Includes comments explaining each part of the policy.

Return only the Rego policy snippet (no extra text).
"""
    # Real call (commented out if you don't have a valid key):
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0
    )
    rego_code = response["choices"][0]["message"]["content"]
    return rego_code
    """
    
    # For demonstration, let's just return a static Rego snippet:
    return """package multi_cloud_policy

# Rule: Managers are allowed to approve resource requests.
allow[role] {
    role == "Manager"
    input.action == "approve"
    input.resource == "ResourceRequests"
}

# Rule: Managers are explicitly denied the delete action on resource requests.
deny[role] {
    role == "Manager"
    input.action == "delete"
    input.resource == "ResourceRequests"
}

# Default rule: Deny access if no allow rule matches.
default allow = false
"""

##############################################################################
# 2. Streamlit UI
##############################################################################


st.title("Multi-Cloud Policy Synthesis MVP (Streamlit)")

st.write("""
**Instructions**:  
1. Enter a security requirement for the 'Manager' role (e.g., "Managers can approve but never delete ResourceRequests").  
2. Generate a Rego policy via the LLM.  
3. Translate to AWS IAM JSON.  
4. Verify the policy to ensure no Manager can delete ResourceRequests.  
5. If verification fails, you can re-run generation with an updated prompt.  
""")

requirement_text = st.text_input(
    "Enter high-level security requirement for Manager:",
    value="Managers can approve resource requests but cannot delete them."
)

if st.button("Generate Rego Policy"):
    with st.spinner("Calling LLM to generate Rego policy..."):
        rego_policy = call_llm_for_rego_policy(requirement_text)
    st.success("Rego Policy Generated!")
    st.code(rego_policy, language="rego")

    st.session_state["rego_policy"] = rego_policy  # store in session

# If we have a rego policy in session, let user translate and verify
if "rego_policy" in st.session_state:
    rego_policy = st.session_state["rego_policy"]

    # Translation
    if st.button("Translate to AWS IAM"):
        allow_rules, deny_rules = parse_rego_policy(rego_policy)
        aws_policy_json = generate_aws_iam_policy(allow_rules, deny_rules)
        st.subheader("AWS IAM Policy JSON")
        st.code(aws_policy_json, language="json")
        st.session_state["aws_policy_json"] = aws_policy_json

    # Verification
    if st.button("Verify Policy"):
        allow_rules, deny_rules = parse_rego_policy(rego_policy)
        result = verify_no_manager_delete(allow_rules, deny_rules)
        if result:
            st.success("Verification Passed: Manager cannot delete ResourceRequests.")
        else:
            st.error("Verification Failed: There's a scenario where Manager can delete ResourceRequests!")
            st.write("Consider refining your requirement or prompt and re-generating the policy.")

            if st.button("Refine and Re-generate"):
                # In a real app, you'd feed back the error into the prompt automatically:
                refined_requirement = f"{requirement_text}. Also ensure that Managers are explicitly denied the delete action."
                with st.spinner("Re-calling LLM with refined prompt..."):
                    new_rego = call_llm_for_rego_policy(refined_requirement)
                st.session_state["rego_policy"] = new_rego
                st.experimental_rerun()

