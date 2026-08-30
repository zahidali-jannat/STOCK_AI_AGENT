# Functions that have been used in this project , i wrote it here separetly which will help you to understand it more clearly 


import yfinance as yf
# About Function get_data_change:
"""get_data_change is a function which actually fetch the price of given stock from yahoo finance """
def get_data_change(ticker_symbol="AAPL"):
    stock=yf.Ticker(ticker_symbol)
    stock_closing_price=stock.history(period="1mo")["Close"].diff() # get daily price change data 
    print(stock_closing_price.iloc[-2])




def get_data_change(ticker_symbol : str):
    """ Use this when user specifically ask for daily change in stock price """
    stock=yf.Ticker(ticker_symbol)
    try:

        stock_day_change=stock.history(period="1mo")["Close"].diff() # get daily price change data 
        return stock_day_change.iloc[-2]
    except Exception as e:
        return {f"Error has been occured as {e}"}




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