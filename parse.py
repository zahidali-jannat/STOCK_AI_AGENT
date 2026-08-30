import yfinance as yf

def get_data_change(ticker_symbol="AAPL"):
    stock=yf.Ticker(ticker_symbol)
    stock_closing_price=stock.history(period="1mo")["Close"].diff() # get daily price change data 
    print(stock_closing_price.iloc[-2])

get_data_change("AAPL")