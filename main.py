from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os 
from dotenv import load_dotenv

load_dotenv()
llm=ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retires=2,
    api_key=os.environ.get("GOOGLE_API_KEY")
)

