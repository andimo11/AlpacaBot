import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import time
from datetime import date
import numpy as np
import time
from pytz import timezone
import requests, bs4, re, time
from bs4 import BeautifulSoup

# APCA_API_BASE_URL: 'https://api.alpaca.markets',
# APCA_API_KEY_ID: 'xxx',
# APCA_API_SECRET_KEY: 'xxx'

#simulation
class Wallet:
    gains = 0
    losses = 0
    money = 0
    def __init__(self, money):
        self.money = money
testWallet = Wallet(400000)

#API connection & account info
api = tradeapi.REST(
    'xxx',
    'xxx',
    api_version='v2'
)
account = api.get_account()
api.list_positions()

#@@@@@Functions@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def buy(s, q, si, ty, tif):
    api.submit_order(
        symbol=s,
        qty=q,
        side=si,
        type=ty,
        time_in_force=tif
    )

def sell(s, q, si, ty, tif, lp):
    api.submit_order(
        symbol=s,
        qty=q,
        side=si,
        type=ty,
        time_in_force=tif,
        limit_price=lp
    )

def getCompanyData(comp, tm, lim):
    barset = api.get_barset(comp, tm, limit=lim)
    open = barset[comp][0].o
    close = barset[comp][-1].c
    print('open ', open)
    print('close ', close)
    # return str(barset)

def getAveragePrice(comp, tm, lim):
    a = 0
    barset = api.get_barset(comp, tm, limit=lim)
    for b in barset[comp]:
        a += b.h
    return (a/lim)
# print('time ',b.t) # print('high ',b.h) # print('low ',b.l)

def getCurrentPrice(comp):
    barset = api.get_barset(comp, '1Min', limit=1)
    print('current price of ', comp, ' is ')
    for b in barset[comp]:
        print('high ',b.h)
        print('low ',b.l)

#set parameters and check for buy/pass
def checkStockHistory(comp):
    tenDayAvg = getAveragePrice(comp, 'minute', 1000)
    hundDayAvg = getAveragePrice(comp, 'day', 52)
    currentP = getCurrentPrice(comp)
    print(tenDayAvg)
    print(hundDayAvg)
    return True

# def getAccountInfo():
#     print('cash',str(account.cash))
#####doesn't work
#     print('symbol',str(activity.symbol))
#     print('quantity',str(activity.cum_qty))
#     print('price',str(activity.price))

def scrapeGainers():
    companies = list()
    r = requests.get('https://ca.finance.yahoo.com/screener/predefined/day_gainers/')
    c = r.content
    soup = BeautifulSoup(c, features="lxml")
    main_content = soup.find('div', attrs = {'class': 'Pos(r)', 'id': 'scr-res-table'})
    for node in main_content.find_all('a'):
        companies.append(node.text)
    return companies

def symBuy(stock):
    #walletMoney - stock limit_price
    #add stock to list of assets
    print('order ', stock,' filled')

def analyzeSet(companies):
    for i in companies:
        if checkStockHistory(i):
            symBuy(i)
            print(i,' sent to order')


#/@@@@@@@@@@@@@@@End functions@@@@@@@@@@@@@@@@@@@@@@

#!!!!!!!!!!!!!!!TESTYYY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#/!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

###############this code starts the script 15 minutes after the stock opens#####
#market time info
clock = api.get_clock()
today = datetime.today().strftime('%Y-%m-%d')
calendar = api.get_calendar(start=today, end=today)[0]

open_time = datetime.strptime(str(calendar.open), '%H:%M:%S')
close_time = datetime.strptime(str(calendar.close), '%H:%M:%S')

#my time info
fmt = '%H:%M:%S'
eastern = timezone('US/Eastern') #my time # naive_time = datetime.now() # print(naive_dt.strftime(fmt)) #15:21:00
#eastern time
east_time = datetime.now(eastern) # print(loc_dt.strftime(fmt)) #19:21:00
time_now = east_time.strftime('%H:%M:%S')

##############end time data##############################################

#$*$*$*$*$*$*$*$*$*$*$*$*Beginning of program*$*$*$*$*$*$*$*$*$*$*$*$*
while True:
    if clock.is_open:
        # time.sleep(15*60)
        while clock.is_open:
            #if listOfAssets != 0:
                #analyzeAssets() #check to see if I should sell
            print('Market open: ', time_now)
            # print (getCompanyData('FB', 'day', 1000))
            companies = scrapeGainers()
            analyzeSet(companies)
            print(getAveragePrice('AAPL','1Min', 1))
            print('Market closes at ', close_time)
            #letsss codeeee baby
            #goal: calculate the 5 and 100 day average price
            #check stocks
            #buy some
            #sell some
            #make money
            #repeat
            #sell all stocks before market closes
            time.sleep(3)
    else:
        ###header#####
        print('Market closed')
        print('Opens tomorrow at 9:30')
        companies = scrapeGainers()
        analyzeSet(companies)
        ###/endHeader####
        # Wallet.money += 100
        # print(Wallet.money)
        time.sleep(3)
#/$*$*$*$*$*$*$*$*$*$*$*$*$*End of program*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$




#!!!!!!!!!!Trash&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# # Submit a limit order to attempt to sell 1 share of AMD at a
# # particular price ($20.50) when the market opens
# api.submit_order(
#     symbol='AMD',
#     qty=1,
#     side='sell',
#     type='limit',
#     time_in_force='opg',
#     limit_price=20.50
# )


# # Get daily price data for AAPL over the last 5 trading days.
# barset = api.get_barset('AAPL', 'minute', limit=5)
# # aapl_bars = barset['AAPL']
# print(str(aapl_bars))

#how to navigate through bars
# week_open = aapl_bars[0].o
# week_close = aapl_bars[-1].c

# open = barset[comp][0].o
# close = barset[comp][-1].c
# print('open ', open)
# print('close ', close)


# # Get daily price data for AAPL over the last 5 trading days.
# barset = api.get_barset('AAPL', 'day', limit=5)
# aapl_bars = barset['AAPL']
#
# # See how much AAPL moved in that timeframe.
# week_open = aapl_bars[0].o
# week_close = aapl_bars[-1].c
# percent_change = (week_close - week_open) / week_open * 100
# print('AAPL moved {}% over the last 5 days'.format(percent_change))

# # Check if our account is restricted from trading.
# if account.trading_blocked:
#     print('Account is currently restricted from trading.')

# # Check how much money we can use to open new positions.
# print('${} is available as buying power.'.format(account.buying_power))

# # Get a list of all active assets.
# active_assets = api.list_assets(status='active')
# print(active_assets)

# # Filter the assets down to just those on NASDAQ.
# nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
# print(nasdaq_assets)
#
# # Check if AAPL is tradable on the Alpaca platform.
# aapl_asset = api.get_asset('AAPL')
# if aapl_asset.tradable:
#     print('We can trade AAPL.')
#
# # Check if the market is open now.
# clock = api.get_clock()
# print('The market is {}'.format('open.' if clock.is_open else 'closed.'))
#
# # Check when the market was open on Dec. 1, 2018
# date = '2019-12-16'
# calendar = api.get_calendar(start=date, end=date)[0]
# print('The market opened at {} and closed at {} on {}.'.format(
#     calendar.open,
#     calendar.close,
#     date
# ))

# # Submit a market order to buy 1 share of Apple at market price
# api.submit_order(
#     symbol='AAPL',
#     qty=1,
#     side='buy',
#     type='market',
#     time_in_force='gtc'
# )
