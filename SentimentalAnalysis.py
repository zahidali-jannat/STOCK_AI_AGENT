from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
import yfinance as yf
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
import pandas as pd
import numpy as np
load_dotenv()

def calculate_baseline(history):
    # get each date 30 days forward price change 
    total_size=0
    positive_change=0
    for index in history.index[:-30]: # this will exclude atleast last 30 days 
        idx=history.index.get_loc(index) # getting the index of date which is present in history
        prices=history.iloc[idx:idx+31]["Close"] # Getting 30 days ahead data 
        pct_changes=(prices.iloc[-1]-prices.iloc[0])/prices.iloc[0]*100
        print(index, prices.iloc[0], prices.iloc[-1], pct_changes)
        total_size+=1
        if pct_changes > 0:
            positive_change=positive_change+1

    baseline_win_rate=positive_change/total_size*100
    return float(baseline_win_rate)

         
def sentimental_analysis(ticker:str):
    stock=yf.Ticker(ticker)
    history=stock.history(period="5y")
    sma_20 = history['Close'].rolling(window=20).mean()
    history['pct_above_sma'] = (history['Close'] - sma_20) / sma_20 * 100
    history['rsi'] = RSIIndicator(close=history['Close'], window=14).rsi()
    current_rsi_value=history['rsi'].iloc[-1]
    current_pct_changes=history['pct_above_sma'].iloc[-1]
    print(current_rsi_value)
    print(current_pct_changes)
    # Here i created a data frame named Filtered_data_frame which actually stores rsi and pct_above_sma under defined conditions
    filtered_data_frame=history[history['rsi'].between(50, 60) & history['pct_above_sma'].between(2.4,5.6)][['rsi' , 'pct_above_sma']]
    # Print the data frame 
    print(filtered_data_frame)
    # print(type(history))
    if(len(filtered_data_frame)==0):
       return "Nothing Matched Previously"
    # This loop is soo important to comprehend 
    else:
        empty_array = []
        for index , row in filtered_data_frame.iterrows():
            # print(index)
            # print(row["rsi"] , row["pct_above_sma"])
            idx = history.index.get_loc(index)
            prices = history.iloc[idx:idx + 31]["Close"]
            pct_changes=(prices.iloc[-1]-prices.iloc[0])/prices.iloc[0]*100
            
            empty_array.append(pct_changes)

    # lets check probability 
    positive_number=0
    negative_number=0
    for item in empty_array:
        if item>0:
            positive_number=positive_number+1
        else:
            negative_number=negative_number+1
    
    Percentage_of_positive_return=positive_number/np.size(empty_array)*100
    print("Probability of positive return " ,Percentage_of_positive_return )
    basline_percentage=calculate_baseline(history)
    print(basline_percentage)
    winning_ege=Percentage_of_positive_return - basline_percentage
    print("Winning edge is " ,winning_ege)
    # given_date=filtered_data_frame.index[0] # i wrote .loc[0] which will return the whole row , which was actually creating problem so use .index[0]
    # print(type(given_date))
sentimental_analysis("MSFT") 



