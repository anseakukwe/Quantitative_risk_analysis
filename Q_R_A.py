# -*- coding: utf-8 -*-


#Importing the relevant libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,6]

##Loading the stock data to a pandas dataframe
AAPL = pd.read_csv('AAPL_data.csv')
FBK  = pd.read_csv('FB_data.csv')
NFLX = pd.read_csv('NFLX_data.csv')
GOOGL = pd.read_csv('GOOGL_data.csv')
AMZN = pd.read_csv('AMZN_data.csv')


#Performing data manipulation to get the data into its desired structure
#Exploratory data analysis to check if all the data are in the right shapes and structure
AAPL.columns
Apple_close = AAPL[['date','close']]
Apple_close = Apple_close.rename(columns = {"date": "date", "close": "AAPL"})
Apple_close.index

FBK_close = FBK[['date','close']]
FBK_close = FBK_close.rename(columns = {"date": "date", "close": "FBK"})
FBK_close.shape

NFLX_close = NFLX[['date','close']]
NFLX_close = NFLX_close.rename(columns = {"date":"date", "close": "NFLX"})
NFLX_close.describe()

GOOGL_close = GOOGL[['date','close']]
GOOGL_close = GOOGL_close.rename(columns = {"date" : "date", "close": "GOOGL"})

AMZN_close = AMZN[['date','close']]
AMZN_close = AMZN_close.rename(columns = {"date" : "date", "close": "AMZN"})

Portfolio_1 = pd.merge(NFLX_close, FBK_close, on = "date", how = 'outer')
Portfolio_1.index
Portfolio_1 = Portfolio_1.set_index('date')

Portfolio_2 = pd.merge(GOOGL_close, AMZN_close, on = 'date', how = "outer")
Portfolio_2 = Portfolio_2.set_index('date')
Portfolio_2.head()

Portfolio_merge = pd.concat([Portfolio_1, Portfolio_2], axis = 1)
Portfolio_merge.shape

#Visualizing the stock portfolio
Portfolio_merge.plot().set_ylabel('Closing Stock Prices')

#Visualizing the Apple stock
Apple_close = Apple_close.set_index('date')
Apple_close.plot().set_ylabel('Apple Closing Stock Price')

#Calculating apple stock returns
Apple_Stock_returns = Apple_close.pct_change()
Apple_Stock_returns = Apple_Stock_returns.dropna()
Apple_Stock_returns_percent = Apple_Stock_returns*100
#Apple_Stock_returns_sort = Apple_Stock_returns_percent.sort_values(by = ['AAPL'])
Apple_Stock_returns_percent

#Calculating Historical Value at Risk Apple
Apple_VaR95 = np.percentile(Apple_Stock_returns_percent, 5)
Apple_VaR95


#Calculating Portfolio returns
Stock_portfolio_returns = Portfolio_merge.pct_change()
Stock_portfolio_returns

# Assigning weights to portfolio such that since they are four stocks in the Portfolio
#the sum of the weights should always be equal to 1
weights = [0.25, 0.25, 0.25, 0.25]

portfolio_returns = Stock_portfolio_returns.dot(weights)
portfolio_returns = portfolio_returns.dropna()
portfolio_returns_percent = portfolio_returns*100

portfolio_VaR95 = np.percentile(portfolio_returns_percent, 5)
portfolio_VaR95

#Visualizing the Historical Value at risk of both Apple stock and Stock Portfolio
sns.distplot(Apple_Stock_returns_percent, color='r', label='Apple Returns')
sns.distplot(portfolio_returns_percent, color='b', label= 'Stock_Portfolio Returns')
plt.axvline(x=Apple_VaR95, color='r', linestyle='-', label="Apple VaR 95: {0:.2f}%".format(Apple_VaR95))
plt.axvline(x=portfolio_VaR95 , color='g', linestyle='-', label="Stock Portfolio VaR 95: {0:.2f}%".format(portfolio_VaR95))
plt.xlabel('Returns')
plt.ylabel('Probability')
plt.title('Historical Value at Risk')
plt.legend()
plt.show()


#Assigning equal value for starting price for  Apple stock and Stock Portfolio
Starting_price = 170

#Calculating the Monte Carlo value at risk for Apple stock
np.random.seed(44)
simulation = 1000

mean_apple = np.mean(Apple_Stock_returns)
std_apple = np.std(Apple_Stock_returns)
simulated_returns = np.random.normal(mean_apple, std_apple, simulation)
Simulated_Apple_VaR95 = Starting_price*np.percentile(simulated_returns, 5)
print(Simulated_Apple_VaR95)

#Calculating the Monte Carlo value at risk for Stock Portfolio
np.random.seed(44)
simulation = 1000

mean_portfolio = np.mean(portfolio_returns)
std_portfolio = np.std(portfolio_returns)
simulated_returns = np.random.normal(mean_portfolio , std_portfolio , simulation)
Simulated_Stock_portfolio_VaR95 = Starting_price*np.percentile(simulated_returns, 5)
print(Simulated_Stock_portfolio_VaR95)

#Visualizing the Monte Carlo Value at risk of both Apple stock and Stock Portfolio
sns.distplot(Apple_Stock_returns_percent, color='r', label='Apple Returns')
sns.distplot(portfolio_returns_percent, color='b', label= 'Stock_Portfolio Returns')
plt.axvline(x=Simulated_Apple_VaR95 , color='r', linestyle='-', label="Apple Monte Carlo VaR 95: {0:.2f}%".format(Simulated_Apple_VaR95))
plt.axvline(x=Simulated_Stock_portfolio_VaR95, color='g', linestyle='-', label="Stock Portfolio Monte Carlo VaR 95: {0:.2f}%".format(Simulated_Stock_portfolio_VaR95))
plt.xlabel('Returns')
plt.ylabel('Probability')
plt.title('Monte Carlo Value at Risk')
plt.legend()
plt.show()
