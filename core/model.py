from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, api_key = api_key)