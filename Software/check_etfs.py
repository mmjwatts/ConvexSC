import sys, string, os
import finnhub as fh
import time, datetime
import yfinance as yf

sys.path.append("/home/pi/Setup")
import fhapi

api_key=fhapi.APIkey

finnhub_client = fh.Client(api_key=api_key)

class StockTicker(object):
	def __init__(self, type, ticker, current_price, daily_change, daily_change_pc):
		self.type = type
		self.ticker = ticker
		self.current_price = current_price
		self.daily_change = daily_change
		self.daily_change_pc = daily_change_pc

num_tickers = 0
list = []

#with open("/home/pi/Setup/exchanges.txt") as f:	#Open exchange file for reading
#	for line in f: #iterate over each line
#		type, ticker = line.split()
#		list.append( StockTicker(type, ticker, 0, 0, 0))
#		num_tickers = num_tickers + 1

f = open("/home/pi/etf_prices1.txt" , "w")

#Get current time and midnight last night ready for daily changes
today=datetime.date.today()
unix_today=today.strftime("%s")

unix_timenow=int(time.time())
unix_time_prev_midnight=int(unix_today)

etf="QQQ"
c = yf.Ticker(etf)
quote=c.history(period='1d', interval='1m')
quote_now=quote.Open[-1]
quote=c.history(period='2d', interval='1d') #This automatically only gives data for live trading days
quote_yest=quote.Close[-2]
current_price = quote_now
daily_change = quote_now-quote_yest
daily_change_pc = ((quote_now-quote_yest)/quote_yest) * 100

print >> f, "QQQ " + str("{:.2f}".format(current_price)) + " " + str("{:.2f}".format(daily_change)) + " " + str("{:.2f}".format(daily_change_pc)) + "\n"

etf="DIA"
c = yf.Ticker(etf)
quote=c.history(period='1d', interval='1m')
quote_now=quote.Open[-1]
quote=c.history(period='2d', interval='1d') #This automatically only gives data for live trading days
quote_yest=quote.Close[-2]
current_price = quote_now
daily_change = quote_now-quote_yest
daily_change_pc = ((quote_now-quote_yest)/quote_yest) * 100

print >> f, "DIA " + str("{:.2f}".format(current_price)) + " " + str("{:.2f}".format(daily_change)) + " " + str("{:.2f}".format(daily_change_pc)) + "\n"

etf="SPY"
c = yf.Ticker(etf)
quote=c.history(period='1d', interval='1m')
quote_now=quote.Open[-1]
quote=c.history(period='2d', interval='1d') #This automatically only gives data for live trading days
quote_yest=quote.Close[-2]
current_price = quote_now
daily_change = quote_now-quote_yest
daily_change_pc = ((quote_now-quote_yest)/quote_yest) * 100

print >> f, "SPY " + str("{:.2f}".format(current_price)) + " " + str("{:.2f}".format(daily_change)) + " " + str("{:.2f}".format(daily_change_pc)) + "\n"

os.rename("/home/pi/etf_prices1.txt", "/home/pi/etf_prices.txt")

#print "Done"


