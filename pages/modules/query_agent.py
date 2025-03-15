from langchain.agents import initialize_agent, AgentType
from tools.text_to_aql import text_to_aql_to_text
from modules.llm_handler import llm

# Register tool
tools = [text_to_aql_to_text]

# Define agent function
def query_graph(query):
    app = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    # Fix: Ensure the correct input format
    final_state = app.invoke({"input": query})  # <-- Correct input format
    return final_state["output"]  # <-- Ensure we return the correct key
