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

with open("/home/pi/Setup/exchanges.txt") as f:	#Open exchange file for reading
	for line in f: #iterate over each line
		type, ticker = line.split()
		list.append( StockTicker(type, ticker, 0, 0, 0))
		num_tickers = num_tickers + 1

f = open("/home/pi/exchange_prices1.txt" , "w")

#Get current time and midnight last night ready for daily changes
today=datetime.date.today()
unix_today=today.strftime("%s")

unix_timenow=int(time.time())
unix_time_prev_midnight=int(unix_today)

for x in range(num_tickers):
	ticker_to_check = list[x].ticker
	if list[x].type == "Forex":
		#quote=#Use YF in here somehow!!
		c = yf.Ticker(ticker_to_check + "USD=X")
		quote=c.history(period='1d', interval='1m')
		quote_now=quote.Open[-1]
		quote=c.history(period='2d', interval='1d') #This automatically only gives data for live trading days
		quote_yest=quote.Close[-2]
		list[x].current_price = quote_now
		list[x].daily_change = quote_now-quote_yest
		list[x].daily_change_pc = ((quote_now-quote_yest)/quote_yest) * 100
	else:	#Crypto
		crypto_string="BINANCE:" + str(ticker_to_check) + "USDT"
		quote_today=finnhub_client.crypto_candles(crypto_string, '1', unix_timenow-70, unix_timenow-10)
		quote_yest=finnhub_client.crypto_candles(crypto_string, '1', unix_time_prev_midnight-70, unix_time_prev_midnight-10)
		close_yest = quote_yest['c'][-1]
		list[x].current_price = quote_today['c'][-1]
		list[x].daily_change = (list[x].current_price - close_yest)
		list[x].daily_change_pc = ((list[x].daily_change) / close_yest) * 100
	print >> f, list[x].ticker + " " + str(list[x].current_price) + " " + str("{:.2f}".format(list[x].daily_change_pc)) + "\n"

os.rename("/home/pi/exchange_prices1.txt", "/home/pi/exchange_prices.txt")

#print "Done"


