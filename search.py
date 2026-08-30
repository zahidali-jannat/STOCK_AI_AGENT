import yfinance as yf 
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os 
from dotenv import load_dotenv

load_dotenv()
llm=ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    api_key=os.environ.get("GOOGLE_API_KEY")
)



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
    tools=[stock_price ,  get_data_change],
    system_prompt="You are a finance assistant with access to real-time stock prices. "
                   "If the question is about stock prices, use the stock_price tool to get the latest value.",
)
while(True):
    ticker_=input("Enter your ticker sumbol ")
    try:
        result=agent.invoke({"messages": [{"role": "user", "content": ticker_}]})
        final_answer = result["messages"][-1].content[0]["text"]
        print(final_answer)
    except Exception as e:
        print(f"Error incurred as {e}")    
    