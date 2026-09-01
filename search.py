import yfinance as yf 
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os 
from dotenv import load_dotenv
from pydantic import BaseModel ,Field
from typing import Literal, Optional
load_dotenv()
llm=ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    api_key=os.environ.get("GOOGLE_API_KEY")
)


light_agent=ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    api_key=os.environ.get("GOOGLE_API_KEY")
)

# Below code defines the structural output of LLM , it means i want LLM to give result in given defined way 





@tool
def stock_price(ticker_symbol : str)->float:
    """Get the most recent closing price for a stock ticker symbol 'AAPL'."""
    stock=yf.Ticker(ticker_symbol)
    stock_info=stock.history(period="1mo")
    try:
        if stock_info.empty:
            return "This stock is not listed on stock market"
        else:
            response=stock.history(period="1mo")["Close"].iloc[0]  
            return response  
    except Exception as e:
        return "Error accessing Data"


@tool    
def get_data_change(ticker_symbol : str):
    """ Use this when user specifically ask for daily change in stock price """
    stock=yf.Ticker(ticker_symbol)
    try:

        stock_day_change=stock.history(period="1mo")["Close"].diff() # get daily price change data 
        return stock_day_change.iloc[-2]
    except Exception as e:
        return {f"Error has been occured as {e}"}
@tool
def get_52_week_high_low(ticker_symbol:str)->float:
    """ If a user ask for 52 week highest and lowest price """
    stock=yf.Ticker(ticker_symbol)
    stock_history=stock.history(period="1mo")
    try:
        if stock_history.empty:
            return "This stock is not listed on stock market"
        else:
            info=stock.info
            high_52_week=info.get("fiftyTwoWeekHigh")
            low_52_week=info.get("fiftyTwoWeekLow")
            return "52 Week highest or lowest " , high_52_week ,low_52_week
    except Exception as e:
        return f"Error occured as {e}"

agent=create_agent(
    model=llm,
    tools=[stock_price ,  get_data_change , get_52_week_high_low],
    system_prompt="You are a finance assistant with access to real-time stock prices. "
                   "If the question is about stock prices, use the stock_price tool to get the latest value.",
)

TOOL_MAP = {
    "stock_price": stock_price.func,
    "daily_change": get_data_change.func,
    "52w_high_low": get_52_week_high_low.func,
}

# Below code defines the structural output of LLM , it means i want LLM to give result in given defined way 
class Check_info(BaseModel):
    ticker:Optional[str]=Field(description="Stock Ticker Symbol Like AAPL.. eg..MSFT"
                                            "Null if you confidently resolve it")
    data_types=Literal["current_price", "daily_change", "52w_high_low", "unclear"] = Field(
        description="Which kind of data the user wants.")

# next step is execution , how LLM will given answer to it 
structured_output=llm.with_structured_output(Check_info) # Pass Check_info as argument inside with_structured_output

EXTRACTOR_PROMPT = (
    "Extract the stock ticker symbol and the type of data requested from the user's "
    "question. If unsure of the ticker, or it doesn't map cleanly to current_price / "
    "daily_change / 52w_high_low, set data_type to 'unclear'.\n\nUser question: {query}"
)

def format_answer(ticker: str, data_types:str ,value) ->float:
    if data_types=="stock_price":
        return f"{ticker} The current stock price is {value}"
    if(data_types=="daily_change"):
        return f"{ticker} get latest price change {value}"
    if(data_types=="52w_high_low"):
        return f"{ticker} 52_week high {value["52_week_high"]} , low  {value['52_week_low']}"

    
while(True):
    ticker_=input("Ask about Financial Market ")
    try:
        result=agent.invoke({"messages": [{"role": "user", "content": ticker_}]})
        final_answer = result["messages"][-1].content[0]["text"]
        print(final_answer)
    except Exception as e:
        print(f"Error incurred as {e}")    
    