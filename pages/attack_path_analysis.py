import streamlit as st
import sys
import os
# Add the root project directory to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from modules.query_agent import query_graph

st.title("AWS Attack Path Analysis LLM Agent")

# User Input
user_prompt = st.text_area("Enter your LLM Prompt:", placeholder="Describe possible attack paths for AWS resources...")

# Execute Query
if st.button("Analyze Attack Paths"):
    if not user_prompt:
        st.warning("Please enter a prompt")
    else:
        response = query_graph(user_prompt)
        st.subheader("Analysis Result")
        st.write(response)
