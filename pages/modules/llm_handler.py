import os
from langchain.chat_models import ChatOpenAI
from config.settings import OPENAI_API_KEY

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize LLM
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
