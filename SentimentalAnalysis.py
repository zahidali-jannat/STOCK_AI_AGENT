from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
load_dotenv()
client=NewsDataApiClient(os.environ.get("api_key")) 
def get_stock_news(ticker:str):
     """
    Get recent market-related news for a stock.
    Use this when the user asks about recent/latest
    market news, financial news, or stock news for a company.
    """
     response=client.market_api(q=ticker , language="en")
     articles=[]

     for article in response.get("results" , []):
          articles.append(
               {
                    "title":article.get("title"),
                    "description": article.get("description"),
                    "link": article.get("link"),
                    "source": article.get("source_name"),
                    "published": article.get("pubDate")
               }
          ) 

     return articles     

# it returns 