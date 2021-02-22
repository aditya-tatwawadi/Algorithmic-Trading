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

#Style
plt.style.use('fivethirtyeight')

#Load in data
import pandas_datareader as web
import datetime
 
#datetime.datetime is a data type within the datetime module YYYY-MM-DD
start = datetime.datetime(2006, 10, 2)
end = datetime.datetime(2011, 12, 30)
 
#DataReader method name is case sensitive
df = web.DataReader("AAPL", 'yahoo', start, end)
 
#invoke to_csv for df dataframe object from 
#DataReader method in the pandas_datareader library
 
#..\first_yahoo_prices_to_csv_demo.csv must not
#be open in another app, such as Excel
df.to_csv('AAPL_test.csv')

#Visualize the data
AAPL = pd.read_csv('/Users/adityatatwawadi/Desktop/VisualStudio/AlgoTrading/AAPL_test.csv')

#Create simple moving average
SMA100 = pd.DataFrame()
SMA100['Adj Close'] = AAPL['Adj Close'].rolling(window = 100).mean()
SMA30 = pd.DataFrame()
SMA30['Adj Close'] = AAPL['Adj Close'].rolling(window = 30).mean()

#Create a new dataframe to store all data
data = pd.DataFrame()
data['AAPL'] = AAPL['Adj Close']
data['SMA30'] = SMA30['Adj Close']
data['SMA100'] = SMA100['Adj Close']

#Create a function to signal when to buy and sell the asset/ stock
def buy_sell(data):

    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):

        if data['SMA30'][i] > data['SMA100'][i]:
            if flag != 1:
                sigPriceBuy.append(data['AAPL'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)

        elif data['SMA30'][i] < data['SMA100'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['AAPL'][i])
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

    plt.figure(figsize=(12.5, 4.5))
    plt.plot(data['AAPL'], label = 'AAPL', alpha = 0.35)
    plt.plot(data['SMA30'], label = 'SMA30', alpha = 0.35)
    plt.plot(data['SMA100'], label = 'SMA100', alpha = 0.35)
    plt.scatter(data.index, data['Buy_Signal_Price'], label = 'Buy', marker = '^', color = 'green')
    plt.scatter(data.index, data['Sell_Signal_Price'], label = 'Sell', marker = 'v', color = 'red')
    plt.title('Apple Adj. Close History Buy & Sell Signals')

    #Dates of Plot need to be added
    plt.xlabel('Oct 02, 2006 - Dec 30, 2011')
    plt.ylabel('Adj. Close Price USD ($)')
    plt.legend(loc = 'upper left')
    plt.show()
    return True

visualize_data()