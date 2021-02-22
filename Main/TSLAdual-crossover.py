#Dual Moving average crossover strategy
"""
Strategy - when a short-term average crosses a long-term average.
Signal used to identify that momentum is shifting in the direction of short-term average.
Buy signal generated when the short-term avg crosses long term avg & rises above. Vice-versa for sell signal
"""

#Import dependecies
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime

#Style
plt.style.use('fivethirtyeight')

#datetime.datetime is a data type within the datetime module YYYY-MM-DD
start = datetime.datetime(2019, 1, 1)
end = datetime.datetime(2021, 1, 1)
 
#DataReader method name is case sensitive. 
#N.b. Ticker symbol can be changed. Includes Yahoo API
df = web.DataReader("TSLA", 'yahoo', start, end)
 
#invoke to_csv for df dataframe object from 
#DataReader method in the pandas_datareader library
 
#..\first_yahoo_prices_to_csv_demo.csv must not
#be open in another app, such as Excel
df.to_csv('TSLA_2019-2021.csv')

#Visualize the data - User should use their own desired pathname
TSLA = pd.read_csv('/Users/adityatatwawadi/Desktop/VisualStudio/AlgoTrading/Main/TSLA_2019-2021.csv')

#Create simple moving average
def moving_average():

    global SMA30
    global SMA100

    SMA100 = pd.DataFrame()
    SMA100['Adj Close'] = TSLA['Adj Close'].rolling(window = 100).mean()
    SMA30 = pd.DataFrame()
    SMA30['Adj Close'] = TSLA['Adj Close'].rolling(window = 30).mean()

    return True

moving_average()

#Create a new dataframe to store all data
data = pd.DataFrame()
data['TSLA'] = TSLA['Adj Close']
data['SMA30'] = SMA30['Adj Close']
data['SMA100'] = SMA100['Adj Close']

#Create a function to signal when to buy and sell the asset/ stock
def buy_sell(data):

    sigPriceBuy = []
    sigPriceSell = []

    #Flag is an indicator whether to buy or sell
    flag = -1

    for i in range(len(data)):

        if data['SMA30'][i] > data['SMA100'][i]:
            if flag != 1:
                sigPriceBuy.append(data['TSLA'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)

        elif data['SMA30'][i] < data['SMA100'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['TSLA'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)

        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return (sigPriceBuy, sigPriceSell)

#Store the buy and sell data into a variable
buy_sell = buy_sell(data)
data['Buy_Signal_Price'] = buy_sell[0]
data['Sell_Signal_Price'] = buy_sell[1]

#Visualize data & strategy to buy & sell stock
def visualize_data():

    #Plots the 3 trendlines
    plt.figure(figsize=(12.5, 4.5))
    plt.plot(data['TSLA'], label = 'TSLA', alpha = 0.35)
    plt.plot(data['SMA30'], label = 'SMA30', alpha = 0.35)
    plt.plot(data['SMA100'], label = 'SMA100', alpha = 0.35)
    plt.scatter(data.index, data['Buy_Signal_Price'], label = 'Buy', marker = '^', color = 'green')
    plt.scatter(data.index, data['Sell_Signal_Price'], label = 'Sell', marker = 'v', color = 'red')
    plt.title('Tesla Adj. Close History Buy & Sell Signals')

    #Dates of Plot need to be added
    plt.xlabel('Jan 01, 2019 - Jan 01, 2021')
    plt.ylabel('Adj. Close Price USD ($)')
    plt.legend(loc = 'upper left')
    plt.show()

    return True

visualize_data()