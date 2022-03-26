
import sys, string, os
import finnhub as fh
import time, datetime

sys.path.append("/home/pi/Setup")
import fhapi

api_key=fhapi.APIkey

finnhub_client = fh.Client(api_key=api_key)

class StockTicker(object):
	def __init__(self, type, ticker, quantity, open_price, leverage, current_price, daily_change, total_profit, daily_profit, pf_proportion, total_change, total_change_pc):
		self.type = type
		self.ticker = ticker
		self.quantity = quantity
		self.open_price = open_price
		self.leverage = leverage
		self.current_price = current_price
		self.daily_change = daily_change
		self.total_profit = total_profit
		self.daily_profit = daily_profit
		self.pf_proportion = pf_proportion
		self.total_change = total_change
		self.total_change_pc = total_change_pc

num_tickers = 0
list = []

with open("/home/pi/Setup/portfolio.txt") as f:	#Open portfolio file for reading
	for line in f: #iterate over each line
		type, ticker, quantity, open_price, leverage = line.split()
		quantity = float(quantity.replace(',',''))
		open_price = float(open_price.replace(',',''))
		leverage = float(leverage)
		list.append( StockTicker(type, ticker, quantity, open_price, leverage, 0, 0, 0, 0, 0, 0, 0))
		num_tickers = num_tickers + 1

f = open("/home/pi/portfolio_perf1.txt" , "w")
#print "Checking " + str(num_tickers) + " tickers"

total_investment = 0

#Get current time and midnight last night ready for crypto prices
today=datetime.date.today()
unix_today=today.strftime("%s")

unix_timenow=int(time.time())
unix_time_prev_midnight=int(unix_today)


for x in range(num_tickers):
	ticker_to_check = list[x].ticker
	if list[x].type == "Stock":
		quote=finnhub_client.quote(ticker_to_check)
		list[x].current_price = quote['c']
		list[x].daily_change = quote['d']
	else:	#Crypto
		crypto_string="BINANCE:" + str(ticker_to_check) + "USDT"
		quote_today=finnhub_client.crypto_candles(crypto_string, '1', unix_timenow-70, unix_timenow-10)
                quote_yest=finnhub_client.crypto_candles(crypto_string, '1', unix_time_prev_midnight-70, unix_time_prev_midnight-10)
                close_yest = quote_yest['c'][-1]
                list[x].current_price = quote_today['c'][-1]
                list[x].daily_change = (list[x].current_price - close_yest)
	list[x].total_profit = (list[x].quantity * list[x].current_price) - (list[x].quantity * list[x].open_price)
	list[x].daily_profit = (list[x].quantity * list[x].daily_change)
	list[x].total_change = (list[x].current_price - list[x].open_price)
	list[x].total_change_pc = (list[x].total_change / list[x].open_price) * 100
	total_investment = total_investment + ((list[x].quantity * list[x].open_price)/list[x].leverage)
#	print >> f, list[x].ticker + " " + str(list[x].quantity) + " " + str(list[x].open_price) + " " + str(list[x].current_price) + " " + str(list[x].daily_change) + "\n"
	print >> f, list[x].type + " " + list[x].ticker + " " + str(list[x].current_price) + " " + str(list[x].total_change) + " " + str("{:.2f}".format(list[x].total_change_pc)) + "\n"

#Now update proportion fields (proportion of TODAY's portfolio
#Update overall performance
total_pf_profit = 0
daily_pf_profit = 0
daily_pf_profit_pc = 0

for x in range(num_tickers):
	list[x].pf_proportion = (list[x].quantity * list[x].current_price) / total_investment
	total_pf_profit = total_pf_profit + list[x].total_profit
	daily_pf_profit = daily_pf_profit + list[x].daily_profit

current_pf_value = total_investment + total_pf_profit
daily_pf_profit_pc = (daily_pf_profit / (current_pf_value - daily_pf_profit)) * 100
total_pf_profit_pc = (total_pf_profit / total_investment)*100

f = open("/home/pi/portfolio_summary.txt" , "w")
print >> f, str(round(total_investment,2)) + " " + str(round(current_pf_value,2)) + " " + str(round(total_pf_profit,2)) + " " + str(round(total_pf_profit_pc,2)) + " " + str(round(daily_pf_profit,2)) + " " + str(round(daily_pf_profit_pc,2)) + "\n"

os.rename("/home/pi/portfolio_perf1.txt", "/home/pi/portfolio_perf.txt")

#print "Done"


