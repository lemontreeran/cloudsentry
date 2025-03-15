import streamlit as st

# OpenAI API Key
OPENAI_API_KEY = st.secrets.openai.api_key

# ArangoDB Connection Details
ARANGO_ENDPOINT = "https://60741633f350.arangodb.cloud:8529"
ARANGO_DATABASE = "cloudsentry"
ARANGO_USERNAME = "cloudsentry"
ARANGO_PASSWORD = st.secrets.arango.root_password
